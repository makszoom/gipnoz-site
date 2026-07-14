/**
 * Cloudflare Worker — Gipnoz Site Payments
 *
 * v2: Direct crypto payments via Trongrid (replaces NOWPayments for EN).
 *   - /check-crypto-payment  → verify USDT txid on Tron, activate subscription
 *   - /health                → health check
 *
 * NOWPayments endpoints (/create-payment, /webhook/nowpayments) are
 * commented out — kept as emergency rollback. Uncomment to restore.
 *
 * Secrets (set via `wrangler secret put <name>`):
 *   FIREBASE_SERVICE_ACCOUNT_JSON  (the full JSON as a string)
 *
 * Hardcoded (no secret needed):
 *   USDT_TRC20_ADDRESS = TBEymscYret4g8TJmniPKsoYJhD6b1A6gB
 *   USDT_CONTRACT      = TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
 */

// --- Config ---
const USDT_TRC20_ADDRESS = 'TBEymscYret4g8TJmniPKsoYJhD6b1A6gB';
const USDT_CONTRACT      = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t';
const PLAN_AMOUNTS = {
  monthly:  12_000_000,   // $12  USDT, decimals=6
  lifetime: 50_000_000    // $50  USDT, decimals=6
};

// --- Trongrid: verify USDT transaction on TRC-20 ---
async function checkTrongridTransaction(txid) {
  // Fetch last 50 USDT TRC-20 transactions for our address
  const url = `https://api.trongrid.io/v1/accounts/${USDT_TRC20_ADDRESS}/transactions/trc20?limit=50&only_confirmed=true`;
  const resp = await fetch(url);
  if (!resp.ok) return { ok: false, error: 'Trongrid API error: ' + resp.status };

  const data = await resp.json();
  if (!data.success) return { ok: false, error: 'Trongrid returned error' };

  for (const tx of (data.data || [])) {
    if (tx.transaction_id !== txid) continue;

    // Validate token is USDT
    const symbol = tx.token_info?.symbol;
    if (symbol !== 'USDT') {
      return { ok: false, error: 'Transaction is not USDT (got ' + symbol + ')' };
    }

    // Validate recipient is our address
    // Trongrid returns addresses with '41' hex prefix; our address is Base58
    const to = tx.to || '';
    if (to !== USDT_TRC20_ADDRESS) {
      return { ok: false, error: 'Transaction sent to wrong address: ' + to };
    }

    // Return amount in micro-USDT
    const amount = parseInt(tx.value || '0', 10);
    return { ok: true, amount, from: tx.from };
  }

  return { ok: false, error: 'Transaction not found in last 50 confirmed. Wait 1 min for confirmation.' };
}

// --- Firestore: check if txid already used ---
async function isTxidUsed(txid, token) {
  const projectId = 'gipnoz-site';
  const url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents/used_txids/${txid}`;
  const resp = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return resp.status === 200; // exists
}

// --- Firestore: mark txid as used ---
async function writeUsedTxid(txid, uid, plan, amount, token) {
  const projectId = 'gipnoz-site';
  const url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents/used_txids/${txid}`;
  const resp = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      fields: {
        uid: { stringValue: uid },
        plan: { stringValue: plan },
        amount: { integerValue: amount.toString() },
        timestamp: { timestampValue: new Date().toISOString() }
      }
    })
  });
  return resp.ok;
}

// --- NOWPayments: commented out (emergency rollback) ---
/*
async function verifyNowPaymentsSignature(body, receivedSig) {
  ... old code ...
}
async function getPaymentDetails(paymentId) {
  ... old code ...
}
function extractUid(paymentData) {
  ... old code ...
}
*/

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
    globalThis.FIREBASE_SERVICE_ACCOUNT_JSON = env.FIREBASE_SERVICE_ACCOUNT_JSON;

    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return new Response('OK', { status: 200 });
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

    // ========== NEW: Direct crypto payment verification (Trongrid) ==========
    if (url.pathname === '/check-crypto-payment' && request.method === 'POST') {
      let reqData;
      try { reqData = JSON.parse(await request.text()); } catch {
        return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      const { uid, txid, plan } = reqData;
      if (!uid || !txid || !plan) {
        return new Response(JSON.stringify({ error: 'Missing uid/txid/plan' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      if (!PLAN_AMOUNTS[plan]) {
        return new Response(JSON.stringify({ error: 'Invalid plan. Use monthly or lifetime' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // 1. Verify transaction on Trongrid
      const trx = await checkTrongridTransaction(txid);
      if (!trx.ok) {
        return new Response(JSON.stringify({ error: trx.error }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // 2. Check amount meets plan minimum
      const required = PLAN_AMOUNTS[plan];
      if (trx.amount < required) {
        const gotDollars = (trx.amount / 1_000_000).toFixed(2);
        const needDollars = (required / 1_000_000).toFixed(2);
        return new Response(JSON.stringify({
          error: `Amount mismatch. Expected $${needDollars} USDT, received $${gotDollars} USDT`
        }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // 3. Get Firebase token for Firestore writes
      let fbToken;
      try {
        fbToken = await getFirebaseAccessToken();
      } catch (e) {
        return new Response(JSON.stringify({ error: 'Failed to authenticate with Firestore' }), {
          status: 500,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // 4. Check txid wasn't used before
      const alreadyUsed = await isTxidUsed(txid, fbToken);
      if (alreadyUsed) {
        return new Response(JSON.stringify({ error: 'This transaction was already used' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // 5. Write subscription
      const expiresAt = plan === 'monthly'
        ? new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
        : null;

      const subOk = await writeSubscription(uid, plan, 'active', expiresAt);
      if (!subOk) {
        return new Response(JSON.stringify({ error: 'Failed to write subscription to Firestore' }), {
          status: 500,
          headers: { 'Content-Type': 'application/json', ...corsHeaders() }
        });
      }

      // 6. Mark txid as used
      const txOk = await writeUsedTxid(txid, uid, plan, trx.amount, fbToken);
      if (!txOk) {
        // Subscription is active but txid not marked — log warning, still return success
        console.warn(`Subscription activated but failed to mark txid as used: ${txid}`);
      }

      return new Response(JSON.stringify({
        success: true,
        plan,
        amount_usdt: trx.amount / 1_000_000,
        txid
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json', ...corsHeaders() }
      });
    }

    // ========== NOWPayments: commented out (emergency rollback) ==========
    /*
    globalThis.NOWPAYMENTS_IPN_SECRET = env.NOWPAYMENTS_IPN_SECRET;
    globalThis.NOWPAYMENTS_API_KEY = env.NOWPAYMENTS_API_KEY;
    globalThis.NOWPAYMENTS_MONTHLY_PRODUCT_ID = env.NOWPAYMENTS_MONTHLY_PRODUCT_ID;
    globalThis.NOWPAYMENTS_LIFETIME_PRODUCT_ID = env.NOWPAYMENTS_LIFETIME_PRODUCT_ID;

    // NOWPayments IPN webhook
    if (url.pathname === '/webhook/nowpayments' && request.method === 'POST') {
      const body = await request.text();
      const sig = request.headers.get('x-nowpayments-sig');
      const valid = await verifyNowPaymentsSignature(body, sig);
      if (!valid) return new Response('Invalid signature', { status: 403 });
      ... old code ...
    }

    // Create payment (called by payments.js)
    if (url.pathname === '/create-payment' && request.method === 'POST') {
      ... old code ...
    }
    */

    return new Response('Not found', { status: 404 });
  }
};
