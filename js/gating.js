/* ===== Gating — Video Paywall =====
 * Hides .lesson-video-player behind auth (+ subscription for EN).
 * RU: logged in → video unlocked (free after registration)
 * EN: logged in + active subscription → video unlocked
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
      : 'Video requires a subscription — $12/month or $50 lifetime.',
    gateSubscribeBtn: isRu ? 'Открыть доступ' : 'Unlock access',
    gateSubscribeHref: isRu ? '/subscribe.html' : '/en/subscribe.html',

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

    var existing = document.querySelector('.lesson-video-gate');
    if (existing) existing.remove();

    player.style.display = 'none';
    var gate = createGate(state);
    player.parentNode.insertBefore(gate, player);
  }

  function showPlayer() {
    var player = document.querySelector('.lesson-video-player');
    if (!player) return;

    var gate = document.querySelector('.lesson-video-gate');
    if (gate) gate.remove();

    player.style.display = '';
  }

  // --- Subscription check via Firestore (EN only) ---
  function checkSubscription(uid, callback) {
    try {
      var db = firebase.firestore();
      db.collection('subscriptions').doc(uid).get().then(function(doc) {
        if (!doc.exists) {
          callback(false);
          return;
        }
        var data = doc.data();
        if (data.status === 'active') {
          if (data.expiresAt) {
            var now = firebase.firestore.Timestamp.now();
            if (data.expiresAt.toMillis() > now.toMillis()) {
              callback(true);
            } else {
              callback(false);
            }
          } else {
            callback(true); // lifetime
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
    if (typeof firebase === 'undefined' || !firebase.auth) {
      setTimeout(init, 200);
      return;
    }

    firebase.auth().onAuthStateChanged(function(user) {
      if (!user) {
        // Not logged in → show login gate
        showGate('login');
      } else if (isRu) {
        // RU: logged in = free access, no subscription check
        showPlayer();
      } else {
        // EN: logged in → check subscription
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
