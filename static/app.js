// Fade-in panel & smooth page transitions
window.addEventListener('DOMContentLoaded', () => {
  const panel = document.querySelector('.content-panel');
  if (panel) panel.classList.add('visible');

  // Smooth page transitions
  document.querySelectorAll('a').forEach(a => {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('http')) return;
    a.addEventListener('click', (e) => {
      if (a.target === '_blank') return;
      e.preventDefault();
      panel.classList.remove('visible');
      setTimeout(() => window.location = href, 300);
    });
  });

  // Animate flash messages (auto dismiss)
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.transition = "opacity 0.5s ease";
      flash.style.opacity = "0";
      setTimeout(() => flash.remove(), 600);
    }, 4000); // auto-dismiss after 4s
  });
});
