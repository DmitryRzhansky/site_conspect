document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("pre code").forEach(function(codeBlock, index) {
    // Создаём обёртку
    let wrapper = document.createElement("div");
    wrapper.classList.add("code-wrapper");
    codeBlock.parentNode.parentNode.insertBefore(wrapper, codeBlock.parentNode);
    wrapper.appendChild(codeBlock.parentNode);

    // Кнопка копирования
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

    wrapper.appendChild(copyButton);
  });
});
