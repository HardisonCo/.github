// HMS-MFE Documentation & Animation Integration 
// Core Vue components for documentation and animated diagrams

export { default as DocViewer } from './DocViewer.vue';
export { default as AnimatedDiagram } from './AnimatedDiagram.vue';
export { default as DocsPage } from './DocsPage.vue';

// Also export interfaces for easier consumption
export interface AnimationStep {
  id: string;
  elements: string[];
  description: string;
}

export interface AnimationConfig {
  diagramContainerId: string;
  steps: AnimationStep[];
  controls: {
    nextBtnId: string;
    prevBtnId: string;
    resetBtnId: string;
    playBtnId: string;
    stepCounterId: string;
    stepDescriptionId: string;
    progressBarId?: string;
  };
  playIntervalMs?: number;
  onStepChange?: (stepIndex: number, step: AnimationStep) => void;
}

export interface DocItem {
  path: string;
  title: string;
  description?: string;
  tags?: string[];
}

export interface DocSection {
  id: string;
  title: string;
  documents: DocItem[];
}

export interface DocsManifest {
  sections: DocSection[];
  defaultDocument?: string;
} 