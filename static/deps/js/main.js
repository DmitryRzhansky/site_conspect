function searchInPage() {
  const query = document.getElementById('search-input').value.trim().toLowerCase();
  const content = document.getElementById('chapter-content');
  if (!query) {
    alert('Введите текст для поиска');
    return;
  }

  // Снимаем старые подсветки
  content.innerHTML = content.innerHTML.replace(/<mark>(.*?)<\/mark>/gi, '$1');

  const text = content.innerText.toLowerCase();
  if (!text.includes(query)) {
    alert('Ничего не найдено на этой странице.');
    return;
  }

  // Экранирование спецсимволов в поисковом запросе
  const escapedQuery = query.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
  const regex = new RegExp(`(${escapedQuery})`, 'gi');

  content.innerHTML = content.innerHTML.replace(regex, '<mark>$1</mark>');
}

