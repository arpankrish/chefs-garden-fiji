document.addEventListener('DOMContentLoaded', () => {
  // 1. Instant Client-Side Catalog Filtering
  const filterPills = document.querySelectorAll('[data-filter-category]');
  const searchInput = document.getElementById('catalog-search-input');
  const availabilitySelect = document.getElementById('catalog-availability-select');
  const intensitySelect = document.getElementById('catalog-intensity-select');
  const cards = document.querySelectorAll('.variety-card');
  const emptyState = document.getElementById('catalog-empty-state');
  const visibleCountEl = document.getElementById('catalog-visible-count');

  let activeCategory = 'all';

  function filterCatalog() {
    if (!cards.length) return;
    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
    const avail = availabilitySelect ? availabilitySelect.value : 'all';
    const intensity = intensitySelect ? intensitySelect.value : 'all';

    let visibleCount = 0;

    cards.forEach((card) => {
      const cardCat = card.dataset.category || '';
      const cardAvail = card.dataset.availability || '';
      const cardIntensity = card.dataset.intensity || '';
      const cardSearchText = (card.dataset.search || '').toLowerCase();

      const matchesCat = activeCategory === 'all' || cardCat === activeCategory;
      const matchesAvail = avail === 'all' || cardAvail === avail;
      const matchesIntensity = intensity === 'all' || cardIntensity === intensity;
      const matchesQuery = !query || cardSearchText.includes(query);

      if (matchesCat && matchesAvail && matchesIntensity && matchesQuery) {
        card.style.display = 'flex';
        visibleCount += 1;
      } else {
        card.style.display = 'none';
      }
    });

    if (visibleCountEl) {
      visibleCountEl.textContent = visibleCount;
    }
    if (emptyState) {
      emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  filterPills.forEach((pill) => {
    pill.addEventListener('click', () => {
      filterPills.forEach((p) => p.classList.remove('active'));
      pill.classList.add('active');
      activeCategory = pill.dataset.filterCategory;
      filterCatalog();
    });
  });

  if (searchInput) searchInput.addEventListener('input', filterCatalog);
  if (availabilitySelect) availabilitySelect.addEventListener('change', filterCatalog);
  if (intensitySelect) intensitySelect.addEventListener('change', filterCatalog);

  // 2. Interactive Chef's Inquiry Tray
  const trayItems = new Map();
  const trayBar = document.getElementById('chef-tray-bar');
  const trayCountEl = document.getElementById('tray-count-badge');
  const trayNamesEl = document.getElementById('tray-names-preview');
  const inquiryTextarea = document.getElementById('id_selected_varieties_summary');
  const trayButtons = document.querySelectorAll('.js-toggle-tray');

  function syncInquiryTray() {
    const count = trayItems.size;
    if (trayCountEl) trayCountEl.textContent = count;

    const names = Array.from(trayItems.values()).map((item) => item.name);
    if (trayNamesEl) {
      trayNamesEl.textContent = names.slice(0, 3).join(', ') + (names.length > 3 ? ` +${names.length - 3} more` : '');
    }

    if (trayBar) {
      if (count > 0) {
        trayBar.classList.add('visible');
      } else {
        trayBar.classList.remove('visible');
      }
    }

    if (inquiryTextarea && count > 0) {
      const lines = Array.from(trayItems.values()).map(
        (item) => `• ${item.name} — Punnet ($${item.punnetPrice} FJD) / Live Tray ($${item.trayPrice} FJD)`
      );
      inquiryTextarea.value = lines.join('\n');
    }

    trayButtons.forEach((btn) => {
      const slug = btn.dataset.slug;
      if (trayItems.has(slug)) {
        btn.textContent = '✓ In Inquiry Tray';
        btn.classList.remove('btn-emerald');
        btn.classList.add('btn-gold');
      } else {
        btn.textContent = '+ Inquiry Tray';
        btn.classList.add('btn-emerald');
        btn.classList.remove('btn-gold');
      }
    });
  }

  trayButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const slug = btn.dataset.slug;
      if (trayItems.has(slug)) {
        trayItems.delete(slug);
      } else {
        trayItems.set(slug, {
          name: btn.dataset.name,
          punnetPrice: btn.dataset.punnet,
          trayPrice: btn.dataset.tray,
        });
      }
      syncInquiryTray();
    });
  });

  // 3. Quick Culinary Spec Sheet Modal
  const modalBackdrop = document.getElementById('spec-modal-backdrop');
  const modalCloseBtn = document.getElementById('spec-modal-close');
  const specTriggers = document.querySelectorAll('.js-open-spec-modal');

  specTriggers.forEach((trigger) => {
    trigger.addEventListener('click', () => {
      if (!modalBackdrop) return;
      document.getElementById('modal-img').src = trigger.dataset.image || '';
      document.getElementById('modal-category').textContent = trigger.dataset.categoryName || '';
      document.getElementById('modal-name').textContent = trigger.dataset.name || '';
      document.getElementById('modal-latin').textContent = trigger.dataset.latin || '';
      document.getElementById('modal-description').textContent = trigger.dataset.description || '';
      document.getElementById('modal-flavor').textContent = trigger.dataset.flavor || '';
      document.getElementById('modal-texture').textContent = trigger.dataset.texture || '';
      document.getElementById('modal-pairings').textContent = trigger.dataset.pairings || '';
      document.getElementById('modal-tip').textContent = trigger.dataset.tip || '';
      document.getElementById('modal-harvest').textContent = `${trigger.dataset.growDays} Days Grow Cycle — ${trigger.dataset.leadTime}`;
      document.getElementById('modal-nutrition').textContent = trigger.dataset.nutrition || '';
      document.getElementById('modal-storage').textContent = `${trigger.dataset.storage} (Shelf life: ~${trigger.dataset.shelfLife} days)`;
      document.getElementById('modal-punnet-price').textContent = `$${trigger.dataset.punnetPrice} FJD (${trigger.dataset.punnetWeight})`;
      document.getElementById('modal-tray-price').textContent = `$${trigger.dataset.trayPrice} FJD (${trigger.dataset.trayLabel})`;
      document.getElementById('modal-detail-link').href = trigger.dataset.detailUrl || '#';

      modalBackdrop.classList.add('open');
    });
  });

  if (modalCloseBtn && modalBackdrop) {
    modalCloseBtn.addEventListener('click', () => modalBackdrop.classList.remove('open'));
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) modalBackdrop.classList.remove('open');
    });
  }

  // 4. Live Image Upload Preview in Studio Form
  const fileInput = document.querySelector('input[type="file"][name="primary_image"]');
  const previewImg = document.getElementById('live-upload-preview');
  if (fileInput && previewImg) {
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (ev) => {
          previewImg.src = ev.target.result;
          previewImg.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }
});
