document.addEventListener("DOMContentLoaded", function() {
  const themeLink = document.getElementById("hljs-theme");
  const toggleButton = document.getElementById("toggle-code-theme");

  if (!toggleButton || !themeLink) return;

  // Чтение из localStorage
  let currentTheme = localStorage.getItem("codeTheme") || "light";

  function setTheme(theme) {
    if (theme === "dark") {
      themeLink.href = "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css";
      toggleButton.textContent = "Светлая тема";
    } else {
      themeLink.href = "//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css";
      toggleButton.textContent = "Тёмная тема";
    }
    localStorage.setItem("codeTheme", theme);
  }

  setTheme(currentTheme);

  toggleButton.addEventListener("click", function() {
    currentTheme = currentTheme === "dark" ? "light" : "dark";
    setTheme(currentTheme);
  });
});
