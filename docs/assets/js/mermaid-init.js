// Initialise Mermaid once the runtime script is loaded.

window.__mermaidReady = new Promise((resolve) => {
  function bootMermaid() {
    if (window.mermaid && typeof window.mermaid.initialize === 'function') {
      window.mermaid.initialize({ startOnLoad: true, theme: 'base' });
      resolve();
    }
  }

  if (document.readyState === 'complete') {
    bootMermaid();
  } else {
    window.addEventListener('load', bootMermaid);
  }
});
