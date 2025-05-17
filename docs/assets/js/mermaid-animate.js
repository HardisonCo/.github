/*
 * Frame-by-frame Mermaid animation helper.
 * Looks for ```mermaid code fences containing lines that start with
 * `%% step:N`.  Each step delineates a key-frame.  The helper renders all
 * frames with Mermaid, then cycles through them every 1.2 s.
 */

(function () {
  const STEP_REGEX = /^%%\s*step:(\d+)/;

  async function start() {
    await window.__mermaidReady;

    const codeBlocks = Array.from(
      document.querySelectorAll('pre code.language-mermaid'),
    );

    // Group sequential frames belonging to the same animation
    const animations = [];
    let current = null;

    codeBlocks.forEach((codeEl) => {
      const firstLine = codeEl.textContent.split('\n')[0];
      const match = firstLine.match(STEP_REGEX);
      if (!match) return; // not a key-framed block

      const stepIndex = Number(match[1]);
      if (stepIndex === 0 || !current) {
        current = { frames: [] };
        animations.push(current);
      }
      current.frames.push(codeEl);
    });

    if (!animations.length) return;

    animations.forEach(({ frames }) => {
      // Create container that will hold all rendered SVGs stacked.
      const container = document.createElement('div');
      container.className = 'mermaid-animate-container';
      container.style.position = 'relative';

      const renderedFrames = [];

      frames.forEach((codeEl) => {
        // Hide original pre > code block so it doesn't show duplicate.
        codeEl.parentElement.style.display = 'none';

        // Create div.mermaid for this frame (strip the step comment).
        const merDiv = document.createElement('div');
        merDiv.className = 'mermaid';
        merDiv.textContent = codeEl.textContent.split('\n').slice(1).join('\n');
        container.appendChild(merDiv);
        renderedFrames.push(merDiv);
      });

      // Insert container right after the first hidden code block.
      frames[0].parentElement.insertAdjacentElement('afterend', container);

      // After Mermaid renders SVGs, iterate frames.
      let active = 0;
      function show(index) {
        renderedFrames.forEach((el, i) => {
          el.style.display = i === index ? 'block' : 'none';
        });
      }

      const readyCheck = setInterval(() => {
        const allReady = renderedFrames.every((d) => d.querySelector('svg'));
        if (allReady) {
          clearInterval(readyCheck);
          show(0);
          setInterval(() => {
            active = (active + 1) % renderedFrames.length;
            show(active);
          }, 1200);
        }
      }, 400);
    });
  }

  if (document.readyState === 'complete') start();
  else window.addEventListener('DOMContentLoaded', start);
})();
