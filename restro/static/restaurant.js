document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");

  loginForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission

      // Dummy authentication logic (Replace with backend logic)
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      if (email === "saksham@gmail.com" && password === "@123") {
          alert("Login successful! Redirecting...");
          window.location.href = "main.html"; // Redirect to index.html
      } else {
          alert("Invalid email or password. Please try again.");
      }
    });
});