// Inject “Live” and “Animate” editor links next to every Mermaid code fence.

(function () {
  function init() {
    const blocks = document.querySelectorAll('pre code.language-mermaid');
    blocks.forEach((code) => {
      const wrap = document.createElement('div');
      wrap.className = 'live-link-wrap';

      const svgUrl =
        'https://mermaid.live/edit#' + encodeURIComponent(code.textContent);
      const animUrl =
        'https://cadbox1.github.io/mermaid-live-animated-editor/#/edit/' +
        btoa(
          JSON.stringify({
            code: code.textContent,
            mermaid: { theme: 'default' },
          }),
        );

      const makeBtn = (title, href) => {
        const a = document.createElement('a');
        a.textContent = title;
        a.href = href;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.className = 'live-link';
        return a;
      };

      wrap.appendChild(makeBtn('📈 Live', svgUrl));
      wrap.appendChild(makeBtn('🎞️ Animate', animUrl));

      const pre = code.parentElement;
      pre.style.position = 'relative';
      pre.appendChild(wrap);
    });
  }

  if (document.readyState === 'complete') init();
  else window.addEventListener('DOMContentLoaded', init);
})();
