const chapters = document.querySelectorAll('.chapter');
const homeSections = document.querySelectorAll('.chapter-nav, .welcome');
const categoryPages = document.querySelectorAll('.category-page');
const pageLoadBar = document.querySelector('.page-load-bar');

function showPageLoad(category) {
  if (!pageLoadBar) return;
  pageLoadBar.dataset.category = category || '';
  pageLoadBar.classList.remove('is-loading');
  void pageLoadBar.offsetWidth;
  pageLoadBar.classList.add('is-loading');
}

function showRoute() {
  if (document.body.classList.contains('inner-page')) {
    return;
  }
  const route = window.location.hash.slice(1) || 'domu';
  const page = document.querySelector(`.category-page[data-category="${route}"]`);
  homeSections.forEach((section) => { section.hidden = Boolean(page); });
  categoryPages.forEach((categoryPage) => { categoryPage.hidden = categoryPage !== page; });
  document.title = page ? `${page.querySelector('.sidebar-kicker').textContent} · ZŠ a MŠ Bolatice` : 'ZŠ a MŠ Bolatice';
}

chapters.forEach((chapter) => {
  const toggle = chapter.querySelector('.chapter-toggle');
  toggle.addEventListener('click', () => {
    showPageLoad(chapter.className.match(/chapter--(\w+)/)?.[1]);
    window.location.href = toggle.dataset.page || '#domu';
  });
  chapter.addEventListener('mouseenter', () => {
    chapters.forEach((otherChapter) => {
      if (otherChapter !== chapter) {
        otherChapter.classList.remove('is-open');
        otherChapter.querySelector('.chapter-toggle').setAttribute('aria-expanded', 'false');
      }
    });
  });
});

document.querySelectorAll('a[href]').forEach((link) => {
  link.addEventListener('click', () => {
    showPageLoad(link.dataset.category || document.body.className.match(/category-(\w+)/)?.[1]);
  });
});

window.addEventListener('hashchange', showRoute);
showRoute();