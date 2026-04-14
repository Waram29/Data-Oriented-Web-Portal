document.addEventListener("DOMContentLoaded", function () {
  const togglePwd = document.getElementById("togglePassword");
  const pwdInput = document.getElementById("passwordInput");

  if (togglePwd && pwdInput) {
    togglePwd.addEventListener("click", function () {
      const type = pwdInput.getAttribute("type") === "password" ? "text" : "password";
      pwdInput.setAttribute("type", type);
      this.classList.toggle("visible");
    });
  }
});

