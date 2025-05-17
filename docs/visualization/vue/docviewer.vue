<template>
  <div class="hms-doc-viewer">
    <div v-if="loading" class="loading">Loading document...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="doc-content" ref="contentRef" v-html="renderedContent"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import MarkdownIt from 'markdown-it';
import MarkdownItAnchor from 'markdown-it-anchor';
import MarkdownItToc from 'markdown-it-toc-done-right';
import DOMPurify from 'dompurify';
import mermaid from 'mermaid';
import { AnimationController } from '../controller';

const props = defineProps<{
  path: string;
  baseUrl?: string;
}>();

const emit = defineEmits<{
  (e: 'loaded', path: string): void;
  (e: 'diagram-mounted', el: HTMLElement): void;
}>();

const loading = ref(true);
const error = ref<string | null>(null);
const markdown = ref('');
const renderedContent = ref('');
const contentRef = ref<HTMLElement | null>(null);

// Initialize markdown-it with plugins
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})
  .use(MarkdownItAnchor, { 
    permalink: true,
    permalinkSymbol: '#',
    permalinkSpace: false
  })
  .use(MarkdownItToc, {
    containerClass: 'toc-container',
    listType: 'ul'
  });

// Process markdown content
const renderMarkdown = async () => {
  if (!markdown.value) return;
  
  try {
    // Render the markdown to HTML
    let html = md.render(markdown.value);
    
    // Sanitize the HTML to prevent XSS
    html = DOMPurify.sanitize(html);
    
    // Update the rendered content
    renderedContent.value = html;
    
    // Wait for Vue to update the DOM
    await nextTick();
    
    // Initialize Mermaid diagrams
    if (contentRef.value) {
      const mermaidDivs = contentRef.value.querySelectorAll('.mermaid');
      
      if (mermaidDivs.length > 0) {
        try {
          mermaid.initialize({
            startOnLoad: false,
            theme: 'neutral',
            securityLevel: 'loose'
          });
          
          await mermaid.run();
          
          // Look for diagrams with animation configs
          mermaidDivs.forEach(async (div) => {
            emit('diagram-mounted', div as HTMLElement);
            
            // Look for animation config
            const configScript = div.nextElementSibling;
            if (configScript && 
                configScript.tagName === 'SCRIPT' && 
                configScript.classList.contains('hms-animation-config')) {
              try {
                const config = JSON.parse(configScript.textContent || '{}');
                
                // Setup animation controls
                const controlsDiv = document.createElement('div');
                controlsDiv.className = 'hms-diagram-controls';
                controlsDiv.innerHTML = `
                  <button id="${div.id}-prev" class="btn-prev">Previous</button>
                  <button id="${div.id}-next" class="btn-next">Next</button>
                  <button id="${div.id}-reset" class="btn-reset">Reset</button>
                  <button id="${div.id}-play" class="btn-play">Play Animation</button>
                  <div id="${div.id}-counter" class="step-counter">Step 0 of 0</div>
                  <div id="${div.id}-description" class="step-description"></div>
                `;
                
                div.parentNode?.insertBefore(controlsDiv, configScript);
                
                // Create animation controller
                const animationConfig = {
                  diagramContainerId: div.id,
                  steps: config.steps || [],
                  controls: {
                    nextBtnId: `${div.id}-next`,
                    prevBtnId: `${div.id}-prev`,
                    resetBtnId: `${div.id}-reset`,
                    playBtnId: `${div.id}-play`,
                    stepCounterId: `${div.id}-counter`,
                    stepDescriptionId: `${div.id}-description`
                  }
                };
                
                // Initialize the controller
                new AnimationController(animationConfig);
              } catch (err) {
                console.error('Failed to parse animation config:', err);
              }
            }
          });
        } catch (err) {
          console.error('Mermaid rendering failed:', err);
        }
      }
    }
  } catch (err) {
    error.value = `Failed to render markdown: ${err}`;
  }
};

// Fetch the markdown file
const fetchMarkdown = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const baseUrl = props.baseUrl || '';
    const response = await fetch(`${baseUrl}${props.path}`);
    
    if (!response.ok) {
      throw new Error(`Failed to load document: ${response.status} ${response.statusText}`);
    }
    
    markdown.value = await response.text();
    await renderMarkdown();
    emit('loaded', props.path);
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err);
  } finally {
    loading.value = false;
  }
};

// Watch for path changes
watch(() => props.path, () => {
  fetchMarkdown();
});

onMounted(() => {
  fetchMarkdown();
});
</script>

<style>
.hms-doc-viewer {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.loading, .error {
  padding: 1rem;
  border-radius: 4px;
}

.loading {
  background-color: #f8f9fa;
  color: #6c757d;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.doc-content {
  line-height: 1.6;
}

.doc-content h1, 
.doc-content h2, 
.doc-content h3, 
.doc-content h4, 
.doc-content h5, 
.doc-content h6 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.doc-content a {
  color: #0366d6;
  text-decoration: none;
}

.doc-content a:hover {
  text-decoration: underline;
}

.doc-content pre {
  background-color: #f6f8fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.doc-content code {
  background-color: #f6f8fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
}

.doc-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
}

.doc-content th, 
.doc-content td {
  border: 1px solid #dfe2e5;
  padding: 0.5rem 1rem;
}

.doc-content th {
  background-color: #f6f8fa;
}

.toc-container {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.hms-diagram-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

button {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ced4da;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

button:hover {
  background-color: #f1f3f5;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.step-counter {
  font-size: 0.875rem;
  color: #6c757d;
  margin-right: 1rem;
}

.step-description {
  flex: 1;
  font-size: 0.875rem;
}
</style> 