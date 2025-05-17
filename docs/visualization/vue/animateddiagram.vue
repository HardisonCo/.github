<template>
  <div class="hms-animated-diagram">
    <div :id="diagramId" class="diagram-container" ref="diagramRef"></div>
    
    <div v-if="hasAnimation" class="controls-container">
      <button 
        :id="`${diagramId}-prev`" 
        class="control-btn" 
        :disabled="!diagramRendered"
        aria-label="Previous step">
        Previous
      </button>
      
      <button 
        :id="`${diagramId}-next`" 
        class="control-btn" 
        :disabled="!diagramRendered"
        aria-label="Next step">
        Next
      </button>
      
      <button 
        :id="`${diagramId}-reset`" 
        class="control-btn" 
        :disabled="!diagramRendered"
        aria-label="Reset animation">
        Reset
      </button>
      
      <button 
        :id="`${diagramId}-play`" 
        class="control-btn" 
        :disabled="!diagramRendered"
        aria-label="Play animation">
        Play Animation
      </button>
      
      <div :id="`${diagramId}-counter`" class="step-counter" aria-live="polite">
        Step 0 of 0
      </div>
      
      <div :id="`${diagramId}-description`" class="step-description" aria-live="polite">
        <!-- Step descriptions will appear here -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import mermaid from 'mermaid';
import { AnimationController } from '../controller';
import { v4 as uuidv4 } from 'uuid';

interface AnimationStep {
  id: string;
  elements: string[];
  description: string;
}

interface AnimationConfig {
  steps: AnimationStep[];
  playIntervalMs?: number;
}

const props = defineProps<{
  diagram: string;
  config?: AnimationConfig;
  theme?: 'default' | 'forest' | 'dark' | 'neutral';
}>();

const emit = defineEmits<{
  (e: 'rendered'): void;
  (e: 'error', error: Error): void;
}>();

const diagramId = ref(`diagram-${uuidv4()}`);
const diagramRef = ref<HTMLElement | null>(null);
const diagramRendered = ref(false);
const controller = ref<AnimationController | null>(null);
const hasAnimation = ref(false);

// Initialize Mermaid and render the diagram
const renderDiagram = async () => {
  if (!diagramRef.value) return;
  
  try {
    // Configure Mermaid
    mermaid.initialize({
      startOnLoad: false,
      theme: props.theme || 'neutral',
      securityLevel: 'loose', // Needed for animation to work with SVG
    });
    
    // Insert the diagram definition
    diagramRef.value.innerHTML = props.diagram;
    diagramRef.value.className = 'mermaid';
    
    // Render the diagram
    await mermaid.run();
    diagramRendered.value = true;
    emit('rendered');
    
    // If animation config is provided, initialize the controller
    if (props.config && props.config.steps && props.config.steps.length > 0) {
      hasAnimation.value = true;
      
      // Create the animation controller
      controller.value = new AnimationController({
        diagramContainerId: diagramId.value,
        steps: props.config.steps,
        controls: {
          nextBtnId: `${diagramId.value}-next`,
          prevBtnId: `${diagramId.value}-prev`,
          resetBtnId: `${diagramId.value}-reset`,
          playBtnId: `${diagramId.value}-play`,
          stepCounterId: `${diagramId.value}-counter`,
          stepDescriptionId: `${diagramId.value}-description`
        },
        playIntervalMs: props.config.playIntervalMs || 3000
      });
    }
  } catch (error) {
    console.error('Mermaid rendering failed:', error);
    emit('error', error instanceof Error ? error : new Error(String(error)));
  }
};

// Cleanup function
const cleanup = () => {
  if (controller.value) {
    // No explicit cleanup needed for AnimationController,
    // but we'll clear the reference
    controller.value = null;
  }
};

// Watch for changes to the diagram prop
watch(() => props.diagram, () => {
  cleanup();
  diagramRendered.value = false;
  
  // Use setTimeout to ensure DOM is updated before re-rendering
  setTimeout(() => {
    renderDiagram();
  }, 0);
});

onMounted(() => {
  renderDiagram();
});

onBeforeUnmount(() => {
  cleanup();
});
</script>

<style>
.hms-animated-diagram {
  margin: 1rem 0;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.diagram-container {
  width: 100%;
  overflow-x: auto;
}

.controls-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.control-btn {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ced4da;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.control-btn:hover:not(:disabled) {
  background-color: #e9ecef;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.step-counter {
  font-size: 0.875rem;
  color: #6c757d;
  margin-left: 0.5rem;
}

.step-description {
  flex: 1;
  font-size: 0.875rem;
  padding: 0 0.5rem;
}

/* Ensure SVG elements adapt to container */
.diagram-container svg {
  max-width: 100%;
  height: auto !important;
}

/* Media query for mobile responsiveness */
@media (max-width: 640px) {
  .controls-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .step-counter, .step-description {
    margin: 0.5rem 0;
  }
  
  .control-btn {
    padding: 0.5rem;
  }
}

/* Apply animation CSS */
@import url('../animation.css');
</style> 