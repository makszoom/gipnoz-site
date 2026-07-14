/**
 * payments.trongrid.js — Direct USDT (TRC-20) payment verification
 *
 * Replaces NOWPayments for EN subscriptions.
 * Users send USDT directly to our address, then submit txid for verification.
 *
 * Requires: auth-core.js (Firebase Auth)
 * Usage: <script src="/js/payments.trongrid.js"></script>
 *        <div id="payment-plans"></div>
 */
(function() {
  'use strict';

  const WORKER_URL = 'https://gipnoz-payments.makszoom85.workers.dev';
  const USDT_ADDRESS = 'TBEymscYret4g8TJmniPKsoYJhD6b1A6gB';
  const RATE_LIMIT_MAX = 5;
  const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000; // 1 hour

  const PLANS = {
    monthly: {
      title: 'Monthly',
      price: '$12',
      period: '/month',
      amountStr: '12',
      features: ['All 18 video lessons', 'Text lessons', 'Hypnosis scripts']
    },
    lifetime: {
      title: 'Lifetime',
      price: '$50',
      period: '',
      amountStr: '50',
      features: ['Everything in Monthly', 'Lifetime access', 'Future lessons'],
      highlighted: true
    }
  };

  // --- Rate limiter (client-side) ---
  function checkRateLimit() {
    var now = Date.now();
    var raw = localStorage.getItem('trongrid_attempts');
    var attempts = raw ? JSON.parse(raw) : [];
    // Filter to last hour
    attempts = attempts.filter(function(t) { return now - t < RATE_LIMIT_WINDOW_MS; });
    if (attempts.length >= RATE_LIMIT_MAX) {
      var oldest = attempts[0];
      var waitMin = Math.ceil((RATE_LIMIT_WINDOW_MS - (now - oldest)) / 60000);
      return { allowed: false, waitMin: waitMin };
    }
    attempts.push(now);
    localStorage.setItem('trongrid_attempts', JSON.stringify(attempts));
    return { allowed: true };
  }

  // --- Copy to clipboard ---
  function copyAddress(btn) {
    navigator.clipboard.writeText(USDT_ADDRESS).then(function() {
      btn.textContent = 'Copied!';
      setTimeout(function() { btn.textContent = 'Copy'; }, 2000);
    }).catch(function() {
      // Fallback for older browsers
      var ta = document.createElement('textarea');
      ta.value = USDT_ADDRESS;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      btn.textContent = 'Copied!';
      setTimeout(function() { btn.textContent = 'Copy'; }, 2000);
    });
  }

  // --- Verify payment via Worker ---
  function verifyPayment(plan, txid, statusEl, btn) {
    var user = firebase.auth().currentUser;
    if (!user) {
      showStatus(statusEl, 'error', 'Please sign in with Google first.');
      return;
    }

    var rate = checkRateLimit();
    if (!rate.allowed) {
      showStatus(statusEl, 'error', 'Too many attempts. Wait ' + rate.waitMin + ' min.');
      return;
    }

    btn.disabled = true;
    showStatus(statusEl, 'loading', 'Looking for transaction on Tron network...');

    fetch(WORKER_URL + '/check-crypto-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ uid: user.uid, txid: txid.trim(), plan: plan })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        showStatus(statusEl, 'success',
          'Payment confirmed! $' + data.amount_usdt + ' USDT received. Redirecting...');
        setTimeout(function() {
          window.location.href = '/en/dashboard.html';
        }, 2000);
      } else {
        showStatus(statusEl, 'error', data.error || 'Verification failed.');
        btn.disabled = false;
      }
    })
    .catch(function(err) {
      showStatus(statusEl, 'error', 'Network error: ' + err.message);
      btn.disabled = false;
    });
  }

  // --- Show status message ---
  function showStatus(el, type, msg) {
    el.className = 'verify-status verify-status-' + type;
    var icon = { loading: '⏳', success: '✅', error: '❌' }[type] || '•';
    el.innerHTML = icon + ' ' + msg;
  }

  // --- Render payment plans ---
  function renderPlans() {
    var container = document.getElementById('payment-plans');
    if (!container) return;

    var html = '<div class="pricing-grid">';
    for (var key in PLANS) {
      var plan = PLANS[key];
      var cls = plan.highlighted ? 'pricing-card pricing-card-featured' : 'pricing-card';
      html += '<div class="' + cls + '">';
      html += '<h3>' + plan.title + '</h3>';
      html += '<div class="pricing-amount"><span class="pricing-price">' + plan.price + '</span>' +
              '<span class="pricing-period">' + plan.period + '</span></div>';
      html += '<ul class="pricing-features">';
      plan.features.forEach(function(f) {
        html += '<li>' + f + '</li>';
      });
      html += '</ul>';

      // Crypto payment box with QR
      var qrData = 'tron:' + USDT_ADDRESS + '?amount=' + (parseInt(plan.amountStr) * 1000000) + '&token=USDT';
      var qrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=' + encodeURIComponent(qrData);

      html += '<div class="crypto-box">';
      html += '<p class="crypto-label">💳 Pay with USDT (TRC-20)</p>';

      // QR code
      html += '<div class="qr-wrapper">';
      html += '<img class="qr-code" src="' + qrUrl + '" alt="Scan to pay USDT">';
      html += '<p class="qr-hint">Scan with your wallet app</p>';
      html += '</div>';

      // Address with copy
      html += '<div class="usdt-address-row">';
      html += '<code class="usdt-address">' + USDT_ADDRESS + '</code>';
      html += '<button class="btn btn-small btn-copy" data-action="copy">Copy</button>';
      html += '</div>';

      // Steps: 3 simple steps
      html += '<ol class="crypto-steps">';
      html += '<li>Scan QR or copy address above</li>';
      html += '<li>Send <strong>$' + plan.amountStr + ' USDT</strong> (TRC-20 network)</li>';
      html += '<li>Copy <strong>txid</strong> from wallet, paste below, click Verify</li>';
      html += '</ol>';

      html += '<input type="text" class="txid-input" placeholder="Paste txid here..." maxlength="64">';
      html += '<button class="btn btn-verify" data-plan="' + key + '">Verify Payment</button>';
      html += '<div class="verify-status"></div>';
      html += '</div>'; // /crypto-box

      // Manual fallback
      html += '<div class="manual-fallback">';
      html += '<a href="#" class="manual-toggle">Paid via P2P / exchange? Request manual activation →</a>';
      html += '<div class="manual-form" style="display:none;">';
      html += '<input type="text" class="manual-method" placeholder="How did you pay? (e.g. Bybit P2P)">';
      html += '<input type="text" class="manual-tg" placeholder="Your Telegram @username">';
      html += '<button class="btn btn-small btn-manual" data-plan="' + key + '">Submit Request</button>';
      html += '<div class="manual-status"></div>';
      html += '</div>';
      html += '</div>';

      html += '</div>'; // /pricing-card
    }
    html += '</div>';
    container.innerHTML = html;

    // Attach handlers
    attachHandlers(container);
  }

  function attachHandlers(container) {
    // Copy buttons
    container.querySelectorAll('.btn-copy').forEach(function(btn) {
      btn.addEventListener('click', function() { copyAddress(btn); });
    });

    // Verify buttons
    container.querySelectorAll('.btn-verify').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var plan = btn.dataset.plan;
        var card = btn.closest('.pricing-card');
        var input = card.querySelector('.txid-input');
        var statusEl = card.querySelector('.verify-status');
        var txid = input.value.trim();

        if (!txid) {
          showStatus(statusEl, 'error', 'Please paste the transaction ID (txid).');
          return;
        }
        if (txid.length < 20) {
          showStatus(statusEl, 'error', 'Txid looks too short. It should be ~64 characters.');
          return;
        }

        verifyPayment(plan, txid, statusEl, btn);
      });
    });

    // Manual fallback toggle
    container.querySelectorAll('.manual-toggle').forEach(function(link) {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        var form = link.parentNode.querySelector('.manual-form');
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
      });
    });

    // Manual submit buttons
    container.querySelectorAll('.btn-manual').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var card = btn.closest('.pricing-card');
        var method = card.querySelector('.manual-method').value.trim();
        var tg = card.querySelector('.manual-tg').value.trim();
        var statusEl = card.querySelector('.manual-status');
        var plan = btn.dataset.plan;

        if (!method || !tg) {
          statusEl.textContent = '❌ Fill in both fields.';
          return;
        }

        var user = firebase.auth().currentUser;
        if (!user) {
          statusEl.textContent = '❌ Please sign in first.';
          return;
        }

        // Write to Firestore manual_payments collection
        var db = firebase.firestore();
        db.collection('manual_payments').doc(user.uid).set({
          plan: plan,
          method: method,
          telegram: tg,
          status: 'pending',
          timestamp: firebase.firestore.FieldValue.serverTimestamp()
        }).then(function() {
          statusEl.textContent = '✅ Request submitted. We will activate your access within 24h.';
          btn.disabled = true;
        }).catch(function(err) {
          statusEl.textContent = '❌ Error: ' + err.message;
        });
      });
    });
  }

  // --- Auto-render ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderPlans);
  } else {
    renderPlans();
  }

  window.renderPaymentPlans = renderPlans;
})();
