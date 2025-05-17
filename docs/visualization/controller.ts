/**
 * Represents a single step in an animation sequence.
 */
interface AnimationStep {
    id: string;          // Unique identifier for the step
    elements: string[];  // CSS selectors for elements to highlight/animate in this step
    description: string; // Text description of the step
    // Optional: Add fields for specific animation classes or parameters if needed
    // e.g., animationClass?: string; pulseTarget?: string;
}

/**
 * Configuration for the AnimationController.
 */
interface AnimationControllerConfig {
    diagramContainerId: string; // ID of the container holding the Mermaid SVG
    steps: AnimationStep[];      // Array of animation steps
    controls: {
        nextBtnId: string;
        prevBtnId: string;
        resetBtnId: string;
        playBtnId: string;
        stepCounterId: string;
        stepDescriptionId: string;
        progressBarId?: string; // Optional progress bar ID
    };
    playIntervalMs?: number;    // Interval for automatic playback (default: 3000ms)
    onStepChange?: (stepIndex: number, step: AnimationStep) => void; // Optional callback
}

/**
 * Controls step-by-step animations for Mermaid diagrams.
 */
export class AnimationController {
    private currentStep: number = 0;
    private steps: AnimationStep[];
    private diagramContainer: HTMLElement;
    private svgElement: SVGElement | null = null;
    private config: AnimationControllerConfig;
    private isPlaying: boolean = false;
    private playInterval: number | null = null;

    private nextBtn: HTMLButtonElement;
    private prevBtn: HTMLButtonElement;
    private resetBtn: HTMLButtonElement;
    private playBtn: HTMLButtonElement;
    private stepCounterEl: HTMLElement;
    private stepDescriptionEl: HTMLElement;
    private progressBarEl: HTMLElement | null = null;

    constructor(config: AnimationControllerConfig) {
        this.config = { playIntervalMs: 3000, ...config }; // Apply defaults
        this.steps = this.config.steps;

        const container = document.getElementById(this.config.diagramContainerId);
        if (!container) {
            throw new Error(`Diagram container with ID '${this.config.diagramContainerId}' not found.`);
        }
        this.diagramContainer = container;

        // Get control elements
        this.nextBtn = document.getElementById(config.controls.nextBtnId) as HTMLButtonElement;
        this.prevBtn = document.getElementById(config.controls.prevBtnId) as HTMLButtonElement;
        this.resetBtn = document.getElementById(config.controls.resetBtnId) as HTMLButtonElement;
        this.playBtn = document.getElementById(config.controls.playBtnId) as HTMLButtonElement;
        this.stepCounterEl = document.getElementById(config.controls.stepCounterId) as HTMLElement;
        this.stepDescriptionEl = document.getElementById(config.controls.stepDescriptionId) as HTMLElement;
        if (config.controls.progressBarId) {
            this.progressBarEl = document.getElementById(config.controls.progressBarId) as HTMLElement;
        }

        this.validateElements();
        this.setupEventListeners();
        this.waitForSvgAndInitialize();
    }

    private validateElements(): void {
        if (!this.nextBtn) throw new Error(`Next button with ID '${this.config.controls.nextBtnId}' not found.`);
        if (!this.prevBtn) throw new Error(`Previous button with ID '${this.config.controls.prevBtnId}' not found.`);
        if (!this.resetBtn) throw new Error(`Reset button with ID '${this.config.controls.resetBtnId}' not found.`);
        if (!this.playBtn) throw new Error(`Play button with ID '${this.config.controls.playBtnId}' not found.`);
        if (!this.stepCounterEl) throw new Error(`Step counter with ID '${this.config.controls.stepCounterId}' not found.`);
        if (!this.stepDescriptionEl) throw new Error(`Step description with ID '${this.config.controls.stepDescriptionId}' not found.`);
        if (this.config.controls.progressBarId && !this.progressBarEl) {
            console.warn(`Progress bar with ID '${this.config.controls.progressBarId}' not found.`);
        }
    }

    private waitForSvgAndInitialize(): void {
        const observer = new MutationObserver((mutations, obs) => {
            const svg = this.diagramContainer.querySelector('svg');
            if (svg) {
                this.svgElement = svg;
                this.renderInitialState();
                obs.disconnect(); // Stop observing once SVG is found
            }
        });

        // Start observing the container for child changes
        observer.observe(this.diagramContainer, { childList: true, subtree: true });

        // Check if SVG is already present
        const existingSvg = this.diagramContainer.querySelector('svg');
        if (existingSvg) {
            this.svgElement = existingSvg;
            this.renderInitialState();
            observer.disconnect();
        }
    }

    private setupEventListeners(): void {
        this.nextBtn.addEventListener('click', () => this.next());
        this.prevBtn.addEventListener('click', () => this.previous());
        this.resetBtn.addEventListener('click', () => this.reset());
        this.playBtn.addEventListener('click', () => this.togglePlay());

        // Optional: Add keyboard listeners
        document.addEventListener('keydown', (e) => {
            // Ensure focus is not on an input field before acting on keydown
            if (document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'SELECT' || document.activeElement?.tagName === 'TEXTAREA') {
                return;
            }
            // Check if the animation container or its children have focus or are visible
            if (!this.diagramContainer.offsetParent) return; // Element is not visible

            switch (e.key) {
                case 'ArrowRight': this.next(); break;
                case 'ArrowLeft': this.previous(); break;
                case 'Home': this.reset(); break;
                case ' ': // Spacebar
                    this.togglePlay();
                    e.preventDefault(); // Prevent page scroll
                    break;
            }
        });
    }

    public next(): void {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.updateAnimation();
            this.updateButtonStates();
        } else if (this.isPlaying) {
            this.stopPlayback();
        }
    }

    public previous(): void {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.updateAnimation();
            this.updateButtonStates();
        }
    }

    public reset(): void {
        this.stopPlayback();
        this.currentStep = 0;
        this.updateAnimation();
        this.updateButtonStates();
    }

    public togglePlay(): void {
        if (this.isPlaying) {
            this.stopPlayback();
        } else {
            this.startPlayback();
        }
    }

    private startPlayback(): void {
        if (this.isPlaying) return;
        this.isPlaying = true;
        this.playBtn.textContent = 'Pause';
        this.playBtn.setAttribute('aria-label', 'Pause animation');

        // Immediately go to next step if not on the last one
        if (this.currentStep < this.steps.length - 1) {
             this.next();
        }

        this.playInterval = window.setInterval(() => {
            if (this.currentStep < this.steps.length - 1) {
                this.next();
            } else {
                this.stopPlayback();
            }
        }, this.config.playIntervalMs);
    }

    private stopPlayback(): void {
        if (!this.isPlaying) return;
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
        this.isPlaying = false;
        this.playBtn.textContent = 'Play Animation';
         this.playBtn.setAttribute('aria-label', 'Play animation sequence');
    }

    private updateAnimation(): void {
        if (!this.svgElement) {
            console.warn('SVG element not available for animation.');
            return;
        }

        const currentStepData = this.steps[this.currentStep];

        // Update progress bar if available
        if (this.progressBarEl) {
            const progressPercent = (this.steps.length > 0) ? ((this.currentStep + 1) / this.steps.length) * 100 : 0;
            this.progressBarEl.style.width = `${progressPercent}%`;
        }

        // Reset styles
        this.svgElement.querySelectorAll('.node, .edgePath').forEach(el => {
            el.classList.remove('highlighted', 'pulse');
            el.classList.add('faded');
        });

        // Apply styles for the current step
        currentStepData.elements.forEach(selector => {
            try {
                 // Attempt to query elements; handle potential complex selectors
                 this.svgElement!.querySelectorAll(selector).forEach(el => {
                    el.classList.remove('faded');
                    el.classList.add('highlighted');

                    // Example: Add pulse to the first element in the step's list
                    if (selector === currentStepData.elements[0]) {
                        el.classList.add('pulse');
                    }
                });
            } catch (e) {
                console.error(`Invalid selector in step ${this.currentStep}: "${selector}"`, e);
            }
        });

        // Update descriptive text
        this.stepDescriptionEl.textContent = currentStepData.description;
        this.stepCounterEl.textContent = `Step ${this.currentStep + 1} of ${this.steps.length}`;

        // Trigger callback if provided
        if (this.config.onStepChange) {
            this.config.onStepChange(this.currentStep, currentStepData);
        }
    }

    private updateButtonStates(): void {
        this.prevBtn.disabled = this.currentStep === 0;
        this.nextBtn.disabled = this.currentStep >= this.steps.length - 1;
    }

    private renderInitialState(): void {
        this.updateButtonStates();
        if (this.steps.length > 0) {
            this.updateAnimation(); // Apply highlighting for the first step
        } else {
            // Handle case with no steps
            this.stepDescriptionEl.textContent = 'No animation steps defined.';
            this.stepCounterEl.textContent = 'Step 0 of 0';
            if (this.progressBarEl) this.progressBarEl.style.width = '0%';
        }
    }
} 