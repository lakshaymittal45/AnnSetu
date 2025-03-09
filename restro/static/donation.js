document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("settingsBtn").addEventListener("click", function () {
      alert("Redirecting to Settings...");
      window.location.href = "settings.html";
  });
  document.getElementById("logoutBtn").addEventListener("click", function () {
      alert("Logging Out...");
      window.location.href = "login.html";
  });
});
