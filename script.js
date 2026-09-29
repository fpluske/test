const chapters = document.querySelectorAll('.chapter');
const homeSections = document.querySelectorAll('.chapter-nav, .home-gallery');
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

const liveSearch = document.querySelector('[data-live-search]');
const liveSearchInput = liveSearch?.querySelector('input');
const liveSearchResults = liveSearch?.querySelector('[data-live-search-results]');
let liveSearchTimer;
const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (character) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  "'": '&#39;',
  '"': '&quot;',
}[character]));

const renderLiveResults = (results, query) => {
  if (!liveSearchResults) return;
  if (!query) {
    liveSearchResults.innerHTML = '';
    liveSearchResults.hidden = true;
    return;
  }
  if (!results.length) {
    liveSearchResults.innerHTML = '<p class="live-search-empty">Nic jsme nenašli.</p>';
  } else {
    liveSearchResults.innerHTML = results.map((result) => `
      <a href="${escapeHtml(result.url)}" class="live-search-result live-search-result--${escapeHtml(result.theme)}">
        <small>${escapeHtml(result.type)}</small>
        <strong>${escapeHtml(result.title)}</strong>
      </a>
    `).join('');
  }
  liveSearchResults.hidden = false;
};

liveSearchInput?.addEventListener('input', () => {
  const query = liveSearchInput.value.trim();
  clearTimeout(liveSearchTimer);
  if (query.length < 2) {
    renderLiveResults([], '');
    return;
  }
  liveSearchTimer = setTimeout(async () => {
    try {
      const response = await fetch(`${liveSearch.action}?q=${encodeURIComponent(query)}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      if (!response.ok) throw new Error('Search request failed');
      const data = await response.json();
      if (liveSearchInput.value.trim() === query) renderLiveResults(data.results, query);
    } catch {
      renderLiveResults([], '');
    }
  }, 250);
});

document.addEventListener('click', (event) => {
  if (liveSearch && !liveSearch.contains(event.target)) renderLiveResults([], '');
});

document.querySelectorAll('[data-slideshow]').forEach((slideshow) => {
  const slides = [...slideshow.querySelectorAll('[data-slide]')];
  const dots = [...slideshow.querySelectorAll('[data-slide-dot]')];
  if (slides.length < 2) return;

  let activeIndex = 0;
  let timer;

  const showSlide = (index) => {
    activeIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => {
      const isActive = slideIndex === activeIndex;
      slide.classList.toggle('is-active', isActive);
      slide.setAttribute('aria-hidden', String(!isActive));
    });
    dots.forEach((dot, dotIndex) => {
      const isActive = dotIndex === activeIndex;
      dot.classList.toggle('is-active', isActive);
      dot.setAttribute('aria-selected', String(isActive));
    });
  };

  const startAutoplay = () => {
    clearInterval(timer);
    timer = setInterval(() => showSlide(activeIndex + 1), 5000);
  };

  slideshow.querySelector('[data-slide-previous]')?.addEventListener('click', () => {
    showSlide(activeIndex - 1);
    startAutoplay();
  });
  slideshow.querySelector('[data-slide-next]')?.addEventListener('click', () => {
    showSlide(activeIndex + 1);
    startAutoplay();
  });
  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      showSlide(Number(dot.dataset.slideDot));
      startAutoplay();
    });
  });
  slideshow.addEventListener('mouseenter', () => clearInterval(timer));
  slideshow.addEventListener('mouseleave', startAutoplay);
  slideshow.addEventListener('focusin', () => clearInterval(timer));
  slideshow.addEventListener('focusout', (event) => {
    if (!slideshow.contains(event.relatedTarget)) startAutoplay();
  });

  startAutoplay();
});