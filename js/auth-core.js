/* ===== Firebase Auth Core ===== */
(function() {
  'use strict';

  // --- Firebase Config (key assembled from parts) ---
  var k1 = "AIzaSy";
  var k2 = "CJ_7qrXDXGGAC6czW5xsPXxvQ_LDnNr3w";
  const firebaseConfig = {
    apiKey: k1 + k2,
    authDomain: "gipnoz-site.firebaseapp.com",
    projectId: "gipnoz-site",
    storageBucket: "gipnoz-site.firebasestorage.app",
    messagingSenderId: "856960072508",
    appId: "1:856960072508:web:fda677ee55e6550935fc39"
  };

  // --- Init Firebase ---
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();

  // --- Language detection ---
  function isEn() {
    return document.documentElement.lang === 'en';
  }

  // --- Update the auth area in the header ---
  function updateAuthLink(user) {
    var link = document.getElementById('auth-link');
    if (!link) {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
          updateAuthLink(user);
        });
      }
      return;
    }

    if (user) {
      // Replace the link with a dropdown
      var name = user.displayName || user.email || 'Profile';
      var dashboardLabel = isEn() ? 'Dashboard' : 'Кабинет';
      var dashboardHref = isEn() ? '/en/dashboard.html' : '/dashboard.html';
      var signOutLabel = isEn() ? 'Sign out' : 'Выйти';

      // Create dropdown HTML
      var dropdown = document.createElement('span');
      dropdown.className = 'auth-dropdown';
      dropdown.innerHTML =
        '<span class="auth-dropdown-toggle" onclick="event.stopPropagation();this.parentElement.classList.toggle(\'open\')">' + name + ' ▾</span>' +
        '<div class="auth-dropdown-menu">' +
          '<a href="' + dashboardHref + '">' + dashboardLabel + '</a>' +
          '<a href="#" class="auth-signout">' + signOutLabel + '</a>' +
        '</div>';

      // Replace the link
      link.parentNode.replaceChild(dropdown, link);

      // Add signout handler
      dropdown.querySelector('.auth-signout').onclick = function(e) {
        e.preventDefault();
        auth.signOut();
      };

      // Close dropdown on outside click
      document.addEventListener('click', function(e) {
        if (!dropdown.contains(e.target)) {
          dropdown.classList.remove('open');
        }
      });

    } else {
      // Show login link
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
    var isEn = lang === 'en';
    var uiConfig = {
      signInSuccessUrl: isEn ? '/en/' : '/',
      signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID
      ],
      tosUrl: isEn ? '/en/about.html' : '/about.html',
      privacyPolicyUrl: isEn ? '/en/about.html' : '/about.html'
    };

    uiConfig.signInFlow = 'popup';

    ui.start('#' + (containerId || 'firebaseui-auth-container'), uiConfig);
  };

})();
