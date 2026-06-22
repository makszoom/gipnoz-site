/**
 * payments.js — Payment buttons for Gipnoz Site
 *
 * Detects language (RU/EN), renders pricing plans,
 * creates NOWPayments invoices via Cloudflare Worker proxy.
 *
 * Requires: auth-core.js (for Firebase UID)
 * Usage: <script src="/js/payments.js"></script>
 *        <div id="payment-plans"></div>
 */

(function() {
  'use strict';

  const LANG = document.documentElement.lang || 'ru';
  const isRu = LANG === 'ru';

  // --- Config ---
  const WORKER_URL = 'https://gipnoz-payments.makszoom85.workers.dev';

  const PLANS = isRu ? [
    {
      id: 'ru-monthly',
      title: 'Месячная подписка',
      price: '99 ₽',
      period: '/мес',
      features: ['Все 37 видеоуроков', 'Текстовые уроки', 'Скрипты гипноза'],
      cta: 'Оплатить картой',
      type: 'yookassa',
      amount: 99,
      highlighted: false
    },
    {
      id: 'ru-lifetime',
      title: 'Навсегда',
      price: '999 ₽',
      period: '',
      features: ['Всё из месячной', 'Доступ навсегда', 'Будущие уроки'],
      cta: 'Оплатить картой',
      type: 'yookassa',
      amount: 999,
      highlighted: true
    }
  ] : [
    {
      id: 'en-monthly',
      title: 'Monthly',
      price: '$12',
      period: '/month',
      features: ['All 18 video lessons', 'Text lessons', 'Hypnosis scripts'],
      cta: 'Pay with Crypto',
      type: 'nowpayments',
      amount: 12,
      highlighted: false
    },
    {
      id: 'en-lifetime',
      title: 'Lifetime',
      price: '$50',
      period: ' once',
      features: ['Everything in Monthly', 'Lifetime access', 'Future lessons'],
      cta: 'Pay with Crypto',
      type: 'nowpayments',
      amount: 50,
      highlighted: true
    }
  ];

  // --- Render plans ---
  function renderPlans(containerId) {
    var container = document.getElementById(containerId || 'payment-plans');
    if (!container) return;

    var html = '<div class="pricing-grid">';
    PLANS.forEach(function(plan) {
      var cls = plan.highlighted ? 'pricing-card pricing-card-featured' : 'pricing-card';
      html += '<div class="' + cls + '">';
      html += '<h3>' + plan.title + '</h3>';
      html += '<div class="pricing-amount"><span class="pricing-price">' + plan.price + '</span><span class="pricing-period">' + plan.period + '</span></div>';
      html += '<ul class="pricing-features">';
      plan.features.forEach(function(f) {
        html += '<li>' + f + '</li>';
      });
      html += '</ul>';
      html += '<button class="btn btn-pay" data-plan="' + plan.id + '" data-type="' + plan.type + '" data-amount="' + plan.amount + '">' + plan.cta + '</button>';
      html += '</div>';
    });
    html += '</div>';

    // YooKassa notice for RU
    if (isRu) {
      html += '<p class="pricing-notice">⚠️ Оплата картой — в разработке. Пока доступна только криптовалюта (USDT) через <a href="/en/subscribe.html">EN-версию</a>.</p>';
    }

    container.innerHTML = html;

    // Attach click handlers
    container.querySelectorAll('.btn-pay').forEach(function(btn) {
      btn.addEventListener('click', function() {
        handlePayment(btn.dataset.type, parseInt(btn.dataset.amount), btn.dataset.plan);
      });
    });
  }

  // --- Handle payment click ---
  function handlePayment(type, amount, planId) {
    if (type === 'yookassa') {
      alert(isRu ? 'Оплата картой пока недоступна. Используйте криптовалюту через EN-версию.' : 'Card payments coming soon. Use crypto via RU version.');
      return;
    }

    if (type === 'nowpayments') {
      // Get Firebase UID
      var user = firebase.auth().currentUser;
      if (!user) {
        alert(isRu ? 'Сначала войдите через Google.' : 'Please sign in with Google first.');
        window.location.href = isRu ? '/login.html' : '/en/login.html';
        return;
      }

      var btn = event.target;
      btn.disabled = true;
      btn.textContent = isRu ? 'Создание платежа…' : 'Creating payment…';

      // Call Worker to create NOWPayments invoice
      fetch(WORKER_URL + '/create-payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          uid: user.uid,
          plan: planId.includes('monthly') ? 'monthly' : 'lifetime',
          amount: amount
        })
      })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.payment_url) {
          window.location.href = data.payment_url;
        } else {
          alert('Error: ' + (data.error || 'Unknown error'));
          btn.disabled = false;
          btn.textContent = planId.includes('monthly')
            ? (isRu ? 'Оплатить' : 'Pay with Crypto')
            : (isRu ? 'Оплатить' : 'Pay with Crypto');
        }
      })
      .catch(function(err) {
        alert('Network error: ' + err.message);
        btn.disabled = false;
        btn.textContent = planId.includes('monthly')
          ? (isRu ? 'Оплатить' : 'Pay with Crypto')
          : (isRu ? 'Оплатить' : 'Pay with Crypto');
      });
    }
  }

  // --- Auto-render on DOM ready ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      renderPlans('payment-plans');
    });
  } else {
    renderPlans('payment-plans');
  }

  // Expose for manual use
  window.renderPaymentPlans = renderPlans;
})();
