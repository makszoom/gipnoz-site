/**
 * Cloudflare Worker — Gipnoz Site Payment Webhooks
 *
 * Handles NOWPayments IPN webhooks.
 * Verifies HMAC-SHA512 signature, extracts user UID from payment metadata,
 * writes subscription status to Firestore via REST API.
 *
 * Deploy: wrangler deploy
 * Secrets (set via `wrangler secret put <name>`):
 *   NOWPAYMENTS_IPN_SECRET
 *   NOWPAYMENTS_API_KEY
 *   FIREBASE_SERVICE_ACCOUNT_JSON  (the full JSON as a string)
 */

// --- HMAC-SHA512 verification for NOWPayments IPN ---
async function verifyNowPaymentsSignature(body, receivedSig) {
  const secret = NOWPAYMENTS_IPN_SECRET;
  if (!secret || !receivedSig) return false;

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-512' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(body));
  const hexSig = Array.from(new Uint8Array(sig))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  return hexSig === receivedSig;
}

// --- Firebase Admin: get OAuth2 access token via JWT assertion ---
async function getFirebaseAccessToken() {
  const sa = JSON.parse(FIREBASE_SERVICE_ACCOUNT_JSON);

  function b64(str) {
    return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }

  const header = { alg: 'RS256', typ: 'JWT' };
  const now = Math.floor(Date.now() / 1000);
  const claims = {
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/datastore',
    aud: sa.token_uri,
    exp: now + 3600,
    iat: now
  };

  const headerB64 = b64(JSON.stringify(header));
  const claimsB64 = b64(JSON.stringify(claims));
  const toSign = `${headerB64}.${claimsB64}`;

  // Parse PEM private key
  const keyData = sa.private_key.replace(/\\n/g, '\n');
  const pemHeader = '-----BEGIN PRIVATE KEY-----';
  const pemFooter = '-----END PRIVATE KEY-----';
  const pemBody = keyData.replace(pemHeader, '').replace(pemFooter, '').replace(/\s/g, '');
  const binaryKey = Uint8Array.from(atob(pemBody), c => c.charCodeAt(0));

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'pkcs8',
    binaryKey,
    { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, encoder.encode(toSign));
  const sigB64 = b64(String.fromCharCode(...new Uint8Array(sig)));

  const jwt = `${toSign}.${sigB64}`;

  const resp = await fetch(sa.token_uri, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=${jwt}`
  });
  const data = await resp.json();
  return data.access_token;
}

// --- Write subscription document to Firestore ---
async function writeSubscription(uid, plan, status, expiresAt) {
  const token = await getFirebaseAccessToken();
  const projectId = 'gipnoz-site';

  const fields = {
    status: { stringValue: status },
    plan: { stringValue: plan },
    updatedAt: { timestampValue: new Date().toISOString() }
  };
  if (expiresAt) {
    fields.expiresAt = { timestampValue: expiresAt };
  }

  const url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents/subscriptions/${uid}`;
  const resp = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ fields })
  });
  return resp.ok;
}

// --- Extract Firebase UID from payment metadata ---
function extractUid(paymentData) {
  if (paymentData.order_id && paymentData.order_id.startsWith('uid:')) {
    return paymentData.order_id.replace('uid:', '');
  }
  return null;
}

// --- Fetch full payment details from NOWPayments API ---
async function getPaymentDetails(paymentId) {
  const resp = await fetch(`https://api.nowpayments.io/v1/payment/${paymentId}`, {
    headers: { 'x-api-key': NOWPAYMENTS_API_KEY }
  });
  if (!resp.ok) return null;
  return resp.json();
}

// --- CORS helper ---
function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
}

// --- Main ---
export default {
  async fetch(request, env) {
    globalThis.NOWPAYMENTS_IPN_SECRET = env.NOWPAYMENTS_IPN_SECRET;
    globalThis.NOWPAYMENTS_API_KEY = env.NOWPAYMENTS_API_KEY;
    globalThis.FIREBASE_SERVICE_ACCOUNT_JSON = env.FIREBASE_SERVICE_ACCOUNT_JSON;
    globalThis.NOWPAYMENTS_MONTHLY_PRODUCT_ID = env.NOWPAYMENTS_MONTHLY_PRODUCT_ID;
    globalThis.NOWPAYMENTS_LIFETIME_PRODUCT_ID = env.NOWPAYMENTS_LIFETIME_PRODUCT_ID;

    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return new Response('OK', { status: 200 });
    }

    // NOWPayments IPN webhook
    if (url.pathname === '/webhook/nowpayments' && request.method === 'POST') {
      const body = await request.text();
      const sig = request.headers.get('x-nowpayments-sig');

      const valid = await verifyNowPaymentsSignature(body, sig);
      if (!valid) {
        return new Response('Invalid signature', { status: 403 });
      }

      let data;
      try { data = JSON.parse(body); } catch {
        return new Response('Invalid JSON', { status: 400 });
      }

      console.log('IPN received:', JSON.stringify(data));

      // Only act on confirmed/finished payments
      const paymentStatus = data.payment_status;
      if (paymentStatus !== 'finished' && paymentStatus !== 'confirmed') {
        return new Response('Ignored — status: ' + paymentStatus, { status: 200 });
      }

      // Get full payment details to extract uid
      const details = await getPaymentDetails(data.payment_id);
      if (!details) {
        return new Response('Failed to fetch payment details', { status: 500 });
      }

      const uid = extractUid(details);
      if (!uid) {
        console.log('No UID found in payment', data.payment_id);
        return new Response('No UID in payment', { status: 200 });
      }

      // Determine plan from price
      const price = parseFloat(details.price_amount || '0');
      let plan, expiresAt;
      if (price <= 5) {
        plan = 'monthly';
        const d = new Date();
        d.setMonth(d.getMonth() + 1);
        expiresAt = d.toISOString();
      } else {
        plan = 'lifetime';
        expiresAt = null;
      }

      const ok = await writeSubscription(uid, plan, 'active', expiresAt);
      if (ok) {
        console.log(`Subscription written: uid=${uid}, plan=${plan}`);
        return new Response('OK', { status: 200 });
      }
      return new Response('Firestore write failed', { status: 500 });
    }

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400'
        }
      });
    }

    // Create payment (called by payments.js)
    if (url.pathname === '/create-payment' && request.method === 'POST') {
      let reqData;
      try { reqData = JSON.parse(await request.text()); } catch {
        return new Response('Invalid JSON', { status: 400, headers: corsHeaders() });
      }

      const { uid, plan, amount } = reqData;
      if (!uid || !plan || !amount) {
        return new Response(JSON.stringify({ error: 'Missing uid/plan/amount' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // Map plan to NOWPayments product
      const productId = plan === 'monthly'
        ? NOWPAYMENTS_MONTHLY_PRODUCT_ID
        : NOWPAYMENTS_LIFETIME_PRODUCT_ID;

      // Create invoice via NOWPayments API
      const invoiceResp = await fetch('https://api.nowpayments.io/v1/invoice', {
        method: 'POST',
        headers: {
          'x-api-key': NOWPAYMENTS_API_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          price_amount: amount,
          price_currency: 'usd',
          pay_currency: 'ltc',
          order_id: 'uid:' + uid,
          order_description: plan === 'monthly'
            ? 'Gipnoz Monthly Subscription'
            : 'Gipnoz Lifetime Access',
          success_url: 'https://gipnozfree.com/dashboard.html',
          cancel_url: 'https://gipnozfree.com/subscribe.html'
        })
      });

      const invoiceData = await invoiceResp.json();
      if (invoiceData.invoice_url) {
        return new Response(JSON.stringify({ payment_url: invoiceData.invoice_url }), {
          status: 200,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }
      return new Response(JSON.stringify({ error: 'Failed to create invoice', detail: invoiceData }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders() }
      });
    }

    return new Response('Not found', { status: 404 });
  }
};
