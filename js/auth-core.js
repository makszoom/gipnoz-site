/* ===== Firebase Auth Core ===== */
(function() {
  'use strict';

  // --- Firebase Config ---
  const firebaseConfig = {
    apiKey: "AIzaSyCJ_7qrXDXGGAC6czW5xsPXxvQ_LDnNr3w",
    authDomain: "gipnoz-site.firebaseapp.com",
    projectId: "gipnoz-site",
    storageBucket: "gipnoz-site.firebasestorage.app",
    messagingSenderId: "856960072508",
    appId: "1:856960072508:web:fda677ee55e6550935fc39"
  };

  // --- Init Firebase ---
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();

  // --- Update the auth link in the header ---
  function updateAuthLink(user) {
    var link = document.getElementById('auth-link');
    // DOM not ready yet — wait for it
    if (!link) {
      document.addEventListener('DOMContentLoaded', function() {
        updateAuthLink(user);
      });
      return;
    }

    if (user) {
      // Logged in — show name, click to logout
      link.textContent = user.displayName || user.email || 'Profile';
      link.href = '#';
      link.onclick = function(e) {
        e.preventDefault();
        if (confirm(link.getAttribute('data-confirm') || 'Sign out?')) {
          auth.signOut();
        }
      };
    } else {
      // Not logged in — show login link
      link.textContent = link.getAttribute('data-label') || 'Sign in';
      link.href = link.getAttribute('data-href') || '/login.html';
      link.onclick = null;
    }
  }

  // --- Auth State Listener ---
  auth.onAuthStateChanged(function(user) {
    updateAuthLink(user);
  });

  // --- FirebaseUI Config (used on login.html) ---
  window.initFirebaseUI = function(containerId, lang) {
    var ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);
    var uiConfig = {
      signInSuccessUrl: '/',
      signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID
      ],
      tosUrl: '/about.html',
      privacyPolicyUrl: '/about.html'
    };

    if (lang === 'ru') {
      uiConfig.signInFlow = 'popup';
    }

    ui.start('#' + (containerId || 'firebaseui-auth-container'), uiConfig);
  };

})();
