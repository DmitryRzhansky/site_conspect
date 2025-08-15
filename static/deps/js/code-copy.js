document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("pre code").forEach(function(codeBlock) {
    // Создаём обёртку
    let wrapper = document.createElement("div");
    wrapper.classList.add("code-wrapper");
    codeBlock.parentNode.parentNode.insertBefore(wrapper, codeBlock.parentNode);
    wrapper.appendChild(codeBlock.parentNode);

    // Создаём кнопку копирования
    let copyButton = document.createElement("button");
    copyButton.classList.add("copy-btn");
    copyButton.textContent = "Копировать";

    copyButton.addEventListener("click", function() {
      let text = codeBlock.innerText;
      navigator.clipboard.writeText(text).then(() => {
        copyButton.textContent = "Скопировано!";
        setTimeout(() => { copyButton.textContent = "Копировать"; }, 2000);
      });
    });

    // Создаём кнопку переключения темы
    let themeButton = document.createElement("button");
    themeButton.classList.add("copy-btn");
    themeButton.style.right = "100px"; // Позиционируем слева от кнопки копирования
    themeButton.id = "toggle-code-theme";
    themeButton.textContent = "Тёмная тема";

    wrapper.appendChild(copyButton);
    wrapper.appendChild(themeButton);
  });
});