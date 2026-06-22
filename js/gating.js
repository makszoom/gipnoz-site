/* ===== Gating — Video Paywall =====
 * Hides .lesson-video-player behind auth + subscription check.
 * Requires: auth-core.js (Firebase init + auth), firebase-firestore-compat.js
 */
(function() {
  'use strict';

  const LANG = document.documentElement.lang || 'ru';
  const isRu = LANG === 'ru';

  // --- Messages ---
  const MSG = {
    gateLoginTitle: isRu ? 'Войдите, чтобы смотреть видео' : 'Sign in to watch the video',
    gateLoginText: isRu
      ? 'Текст урока — бесплатно. Видео доступно после входа.'
      : 'Lesson text is free. Video requires sign-in.',
    gateLoginBtn: isRu ? 'Войти' : 'Sign in',
    gateLoginHref: isRu ? '/login.html' : '/en/login.html',

    gateSubscribeTitle: isRu ? 'Оформите подписку' : 'Subscribe to watch',
    gateSubscribeText: isRu
      ? 'Видео доступно по подписке — 99 ₽/мес или 999 ₽ навсегда.'
      : 'Video requires a subscription — $10/month or $50 lifetime.',
    gateSubscribeBtn: isRu ? 'Открыть доступ' : 'Unlock access',
    gateSubscribeHref: isRu ? '/donate.html' : '/en/donate.html',

    gateLoading: isRu ? 'Загрузка…' : 'Loading…'
  };

  // --- DOM helpers ---
  function createGate(state) {
    var gate = document.createElement('div');
    gate.className = 'lesson-video-gate';

    var icon = document.createElement('div');
    icon.className = 'lesson-video-icon';
    gate.appendChild(icon);

    var h3 = document.createElement('h3');
    h3.textContent = state === 'login' ? MSG.gateLoginTitle : MSG.gateSubscribeTitle;
    gate.appendChild(h3);

    var p = document.createElement('p');
    p.textContent = state === 'login' ? MSG.gateLoginText : MSG.gateSubscribeText;
    gate.appendChild(p);

    var btn = document.createElement('a');
    btn.className = 'btn';
    btn.textContent = state === 'login' ? MSG.gateLoginBtn : MSG.gateSubscribeBtn;
    btn.href = state === 'login' ? MSG.gateLoginHref : MSG.gateSubscribeHref;
    gate.appendChild(btn);

    return gate;
  }

  function showGate(state) {
    var player = document.querySelector('.lesson-video-player');
    if (!player) return;

    // Remove existing gate if any
    var existing = document.querySelector('.lesson-video-gate');
    if (existing) existing.remove();

    // Hide player, insert gate before it
    player.style.display = 'none';
    var gate = createGate(state);
    player.parentNode.insertBefore(gate, player);
  }

  function showPlayer() {
    var player = document.querySelector('.lesson-video-player');
    if (!player) return;

    // Remove gate
    var gate = document.querySelector('.lesson-video-gate');
    if (gate) gate.remove();

    // Show player
    player.style.display = '';
  }

  // --- Subscription check via Firestore ---
  function checkSubscription(uid, callback) {
    try {
      var db = firebase.firestore();
      db.collection('subscriptions').doc(uid).get().then(function(doc) {
        if (!doc.exists) {
          callback(false);
          return;
        }
        var data = doc.data();
        // Check if subscription is active (status === 'active' and not expired)
        if (data.status === 'active') {
          // If there's an expiry, check it
          if (data.expiresAt) {
            var now = firebase.firestore.Timestamp.now();
            if (data.expiresAt.toMillis() > now.toMillis()) {
              callback(true);
            } else {
              callback(false);
            }
          } else {
            // No expiry = lifetime
            callback(true);
          }
        } else {
          callback(false);
        }
      }).catch(function() {
        callback(false);
      });
    } catch(e) {
      callback(false);
    }
  }

  // --- Main ---
  function init() {
    // Wait for Firebase auth to be ready
    if (typeof firebase === 'undefined' || !firebase.auth) {
      // Retry after a short delay
      setTimeout(init, 200);
      return;
    }

    firebase.auth().onAuthStateChanged(function(user) {
      if (!user) {
        // Not logged in → show login gate
        showGate('login');
      } else {
        // Logged in → check subscription
        checkSubscription(user.uid, function(hasSub) {
          if (hasSub) {
            showPlayer();
          } else {
            showGate('subscribe');
          }
        });
      }
    });
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
