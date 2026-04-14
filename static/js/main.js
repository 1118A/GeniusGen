/* ============================================================
   GeniusGen — main.js
   Dark mode | Toasts | AJAX likes/bookmarks | Notifications
   Infinite scroll | Quiz countdown | Mobile menu
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Dark Mode ──────────────────────────────────────────────
  const root = document.documentElement;
  const themeBtn = document.getElementById('theme-toggle');
  const themeIcon = themeBtn ? themeBtn.querySelector('.theme-icon') : null;

  function applyTheme(theme) {
    root.dataset.theme = theme;
    localStorage.setItem('gg-theme', theme);
    if (themeIcon) themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  const savedTheme = localStorage.getItem('gg-theme') || 'light';
  applyTheme(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
    });
  }

  // ── Toast System ───────────────────────────────────────────
  const toastContainer = document.getElementById('toast-container');

  function showToast(text, level = 'info') {
    if (!toastContainer) return;
    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
    const toast = document.createElement('div');
    toast.className = `toast ${level}`;
    toast.innerHTML = `<span>${icons[level] || icons.info}</span><span class="toast-text">${text}</span>`;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 4500);
  }

  // Render Django messages as toasts
  const djangoMessages = document.getElementById('django-messages');
  if (djangoMessages) {
    djangoMessages.querySelectorAll('span').forEach(el => {
      let level = el.dataset.level || 'info';
      if (level.includes('success')) level = 'success';
      else if (level.includes('error')) level = 'error';
      else if (level.includes('warning')) level = 'warning';
      else level = 'info';
      showToast(el.dataset.text, level);
    });
  }

  window.showToast = showToast;

  // ── Mobile Menu ────────────────────────────────────────────
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
    });
    document.addEventListener('click', e => {
      if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        mobileMenu.classList.remove('open');
      }
    });
  }

  // ── User Dropdown ──────────────────────────────────────────
  const userMenu = document.getElementById('user-menu-toggle');
  if (userMenu) {
    userMenu.addEventListener('click', e => {
      e.stopPropagation();
      userMenu.classList.toggle('active');
    });
    document.addEventListener('click', () => userMenu.classList.remove('active'));
  }

  // ── AJAX Like Toggle ────────────────────────────────────────
  document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (!window.IS_AUTHENTICATED) {
        showToast('Please log in to like posts.', 'info');
        return;
      }
      const postId = btn.dataset.postId;
      try {
        const res = await fetch(`/post/${postId}/like/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': window.CSRF_TOKEN,
            'X-Requested-With': 'XMLHttpRequest',
          },
        });
        const data = await res.json();
        const countEl = btn.querySelector('.like-count');
        if (countEl) countEl.textContent = data.likes_count;
        btn.classList.toggle('active', data.is_liked);
        btn.querySelector('.like-icon').textContent = data.is_liked ? '❤️' : '🤍';
      } catch {
        showToast('Something went wrong.', 'error');
      }
    });
  });

  // ── AJAX Bookmark Toggle ────────────────────────────────────
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (!window.IS_AUTHENTICATED) {
        showToast('Please log in to bookmark posts.', 'info');
        return;
      }
      const postId = btn.dataset.postId;
      try {
        const res = await fetch(`/post/${postId}/bookmark/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': window.CSRF_TOKEN,
            'X-Requested-With': 'XMLHttpRequest',
          },
        });
        const data = await res.json();
        btn.classList.toggle('bookmarked', data.is_bookmarked);
        btn.querySelector('.bookmark-icon').textContent = data.is_bookmarked ? '🔖' : '🏷️';
        showToast(data.is_bookmarked ? 'Bookmarked!' : 'Removed bookmark', 'success');
      } catch {
        showToast('Something went wrong.', 'error');
      }
    });
  });

  // ── Follow Toggle ───────────────────────────────────────────
  const followBtn = document.getElementById('follow-btn');
  if (followBtn) {
    followBtn.addEventListener('click', async () => {
      const username = followBtn.dataset.username;
      try {
        const res = await fetch(`/accounts/follow/${username}/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': window.CSRF_TOKEN },
        });
        const data = await res.json();
        const countEl = document.getElementById('followers-count');
        if (countEl) countEl.textContent = data.followers_count;
        followBtn.textContent = data.is_following ? '✓ Following' : '+ Follow';
        followBtn.classList.toggle('btn-secondary', data.is_following);
        followBtn.classList.toggle('btn-primary', !data.is_following);
      } catch {
        showToast('Something went wrong.', 'error');
      }
    });
  }

  // ── Notification Badge Polling ──────────────────────────────
  const notifBadge = document.getElementById('notif-badge');
  if (notifBadge && window.IS_AUTHENTICATED) {
    function pollNotifications() {
      fetch('/notifications/unread-count/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      })
        .then(r => r.json())
        .then(data => {
          if (data.count > 0) {
            notifBadge.style.display = 'flex';
            notifBadge.textContent = data.count > 99 ? '99+' : data.count;
          } else {
            notifBadge.style.display = 'none';
          }
        })
        .catch(() => {});
    }
    pollNotifications();
    setInterval(pollNotifications, 30000);
  }

  // ── Quiz Countdown Timer ────────────────────────────────────
  const timerDisplay = document.getElementById('quiz-timer');
  if (timerDisplay) {
    let seconds = parseInt(timerDisplay.dataset.seconds, 10);
    const quizForm = document.getElementById('quiz-form');

    const tick = setInterval(() => {
      seconds--;
      const m = Math.floor(seconds / 60).toString().padStart(2, '0');
      const s = (seconds % 60).toString().padStart(2, '0');
      timerDisplay.textContent = `${m}:${s}`;

      if (seconds <= 60) timerDisplay.style.color = 'var(--brand-secondary)';
      if (seconds <= 0) {
        clearInterval(tick);
        showToast('Time\'s up! Submitting...', 'warning');
        if (quizForm) quizForm.submit();
      }
    }, 1000);
  }

  // ── Quiz Builder (dynamic questions) ───────────────────────
  const addQuestionBtn = document.getElementById('add-question-btn');
  const questionsContainer = document.getElementById('questions-container');
  let questionCount = 0;

  if (addQuestionBtn && questionsContainer) {
    function addQuestion() {
      questionCount++;
      const qDiv = document.createElement('div');
      qDiv.className = 'question-builder';
      qDiv.id = `question-block-${questionCount}`;
      qDiv.innerHTML = `
        <div class="question-builder-header">
          <span class="font-bold">Question ${questionCount}</span>
          <button type="button" class="btn btn-danger btn-sm remove-question-btn" data-q="${questionCount}">Remove</button>
        </div>
        <div class="form-group">
          <label class="form-label">Question Text</label>
          <textarea name="question_${questionCount}_text" class="form-control" rows="2" required placeholder="Enter your question..."></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Points</label>
          <input type="number" name="question_${questionCount}_points" class="form-control" value="1" min="1" max="10">
        </div>
        <label class="form-label">Choices (select the correct one)</label>
        ${[1,2,3,4].map(j => `
          <div class="flex items-center gap-2 mb-2">
            <input type="radio" name="question_${questionCount}_correct" value="${j}" ${j===1?'required':''} style="accent-color:var(--brand-primary)">
            <input type="text" name="question_${questionCount}_choice_${j}" class="form-control" placeholder="Choice ${j}" required>
          </div>`).join('')}
      `;
      questionsContainer.appendChild(qDiv);
      document.getElementById('question_count').value = questionCount;
      qDiv.querySelector('.remove-question-btn').addEventListener('click', () => {
        qDiv.remove();
        questionCount--;
        document.getElementById('question_count').value = questionCount;
      });
    }

    addQuestionBtn.addEventListener('click', addQuestion);
    // Add 1 by default if empty
    if (questionsContainer.children.length === 0) addQuestion();
  }

  // ── Smooth navbar hide on scroll ───────────────────────────
  let lastY = 0;
  const navbar = document.getElementById('main-navbar');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y > 80) {
      navbar?.classList.toggle('nav-hidden', y > lastY);
    }
    lastY = y;
  }, { passive: true });

  // ── Tech tag input preview ──────────────────────────────────
  const techInput = document.querySelector('input[name="tech_stack"]');
  const techPreview = document.getElementById('tech-preview');
  if (techInput && techPreview) {
    techInput.addEventListener('input', () => {
      const tags = techInput.value.split(',').map(t => t.trim()).filter(t => t);
      techPreview.innerHTML = tags.map(t => `<span class="tech-tag">${t}</span>`).join('');
    });
  }

  // ── Search autocomplete hint ────────────────────────────────
  const navSearch = document.getElementById('nav-search-input');
  if (navSearch) {
    navSearch.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const form = navSearch.closest('form');
        if (form) form.submit();
      }
    });
  }
});
