# HMS Visualization Vue Components

This directory contains Vue components for integrating the HMS documentation system and animated diagrams into the HMS-MFE Vue application.

## Overview

The components in this directory provide:

1. A documentation viewer that renders Markdown files with support for Mermaid diagrams
2. An animation system for Mermaid diagrams that uses the shared HMS Animation Framework
3. A router configuration for easy integration into Vue Router

## Installation

These components are designed to be used in the HMS-MFE Vue application. To use them:

1. Add the required dependencies to your Vue project:

```bash
npm install markdown-it markdown-it-anchor markdown-it-toc-done-right mermaid dompurify uuid
```

2. Copy or symlink the components and assets:
   - Copy the `src/visualization/vue` directory to your Vue project
   - Copy `src/visualization/animation.css` to your assets directory
   - Copy `src/visualization/controller.ts` to your project

3. Update your router configuration to include the documentation routes:

```typescript
// In your router setup file
import { createRouter, createWebHistory } from 'vue-router';
import { setupDocumentationRoutes } from './path/to/vue/router-setup';

const routes = [
  // Your existing routes
  { path: '/', component: Home },
  // Add documentation routes
  ...setupDocumentationRoutes()
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
```

4. Generate the documentation manifest and animation configs:

```bash
# Copy the scripts
cp scripts/generate-docs-manifest.js scripts/extract-animation-configs.js your-project/scripts/

# Run the scripts
cd your-project
node scripts/generate-docs-manifest.js
node scripts/extract-animation-configs.js
```

## Component Usage

### DocViewer

Renders a Markdown document with support for Mermaid diagrams and animations.

```vue
<template>
  <DocViewer 
    path="docs/system/AGENT_ARCHITECTURE.md"
    baseUrl="/api"
    @loaded="onDocLoaded"
    @diagram-mounted="onDiagramMounted"
  />
</template>

<script setup>
import { DocViewer } from './path/to/vue';

const onDocLoaded = (path) => {
  console.log(`Document loaded: ${path}`);
};

const onDiagramMounted = (element) => {
  console.log('Diagram mounted:', element);
};
</script>
```

### AnimatedDiagram

A standalone component for rendering an animated Mermaid diagram.

```vue
<template>
  <AnimatedDiagram
    :diagram="mermaidCode"
    :config="animationConfig"
    theme="neutral"
    @rendered="onDiagramRendered"
    @error="onError"
  />
</template>

<script setup>
import { ref } from 'vue';
import { AnimatedDiagram } from './path/to/vue';

const mermaidCode = ref(`
graph TD
  A[Start] --> B[Process]
  B --> C[End]
`);

const animationConfig = ref({
  steps: [
    {
      id: 'step1',
      elements: ['#A'],
      description: 'This is the starting point'
    },
    {
      id: 'step2',
      elements: ['#B'],
      description: 'Processing occurs here'
    },
    {
      id: 'step3',
      elements: ['#C'],
      description: 'End of the process'
    }
  ]
});

const onDiagramRendered = () => {
  console.log('Diagram has been rendered');
};

const onError = (error) => {
  console.error('Error rendering diagram:', error);
};
</script>
```

### DocsPage

A complete page component that includes a sidebar navigation and document viewer.

```vue
<template>
  <router-view />
</template>

<script setup>
// The router configuration will handle rendering DocsPage at the /docs path
</script>
```

## Customization

### Styling

The components include basic styling that can be customized:

1. Override CSS variables:

```css
:root {
  --hms-primary-color: #0366d6;
  --hms-secondary-color: #f6f8fa;
  --hms-border-color: #e1e4e8;
  --hms-text-color: #24292e;
  --hms-highlight-color: #ffea7f;
}
```

2. Use scoped CSS to customize specific components:

```vue
<style scoped>
.hms-doc-viewer {
  max-width: 1000px; /* Override the default width */
}

.hms-animated-diagram {
  border: 2px solid #d0d7de; /* Custom border style */
}
</style>
```

### Markdown Rendering

You can customize the Markdown rendering by modifying the `DocViewer.vue` component:

```typescript
// Add more plugins to markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})
  .use(MarkdownItAnchor)
  .use(MarkdownItToc)
  .use(YourCustomPlugin);
```

## Accessibility

The components are designed with accessibility in mind:

- All buttons have appropriate `aria-label` attributes
- Animation step descriptions use `aria-live` regions to announce changes
- Keyboard navigation is supported
- The components respect the user's `prefers-reduced-motion` setting

## Integration with HMS Animation Framework

These components use the HMS Animation Framework (`controller.ts` and `animation.css`) for animating diagrams. The framework provides:

- Step-by-step animation controls
- Highlighting and focusing on diagram elements
- Playback control (play, pause, next, previous)
- Accessibility features

## Troubleshooting

### Common Issues

1. **Mermaid diagrams don't render**: Ensure that the Mermaid library is correctly imported and initialized.

2. **Animation controls don't appear**: Check that the animation configuration has proper steps defined.

3. **CSS not loading**: Verify that `animation.css` is properly imported and accessible.

4. **Document not found**: Ensure the path to the markdown file is correct and the file exists at the specified location.

For additional help, check the console for errors or contact the HMS development team. 