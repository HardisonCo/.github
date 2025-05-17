<template>
  <div class="hms-docs-page">
    <aside v-if="sidebarVisible" class="sidebar">
      <button 
        class="sidebar-toggle mobile-only" 
        @click="sidebarVisible = false"
        aria-label="Close sidebar">
        &times;
      </button>
      
      <div class="sidebar-header">
        <h2>HMS Documentation</h2>
      </div>
      
      <div v-if="loadingManifest" class="loading-message">
        Loading document list...
      </div>
      
      <div v-else-if="manifestError" class="error-message">
        {{ manifestError }}
      </div>
      
      <nav v-else class="doc-nav">
        <div v-for="section in docSections" :key="section.id" class="nav-section">
          <div class="section-header" @click="toggleSection(section.id)">
            <span class="section-icon">
              {{ expandedSections.includes(section.id) ? '▼' : '►' }}
            </span>
            <span>{{ section.title }}</span>
          </div>
          
          <transition name="slide">
            <ul v-if="expandedSections.includes(section.id)" class="doc-list">
              <li v-for="doc in section.documents" :key="doc.path">
                <router-link 
                  :to="`/docs/${doc.path}`"
                  :class="{ active: currentPath === doc.path }">
                  {{ doc.title }}
                </router-link>
              </li>
            </ul>
          </transition>
        </div>
      </nav>
    </aside>
    
    <div class="content-area">
      <div class="top-bar">
        <button 
          class="sidebar-toggle desktop-hidden" 
          @click="sidebarVisible = true"
          aria-label="Open sidebar">
          ☰
        </button>
        
        <div class="document-path">
          {{ documentTitle || currentPath }}
        </div>
      </div>
      
      <main class="document-container">
        <DocViewer 
          :path="currentPath" 
          :baseUrl="baseUrl"
          @loaded="onDocLoaded"
        />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import DocViewer from './DocViewer.vue';

interface DocItem {
  path: string;
  title: string;
  description?: string;
  tags?: string[];
}

interface DocSection {
  id: string;
  title: string;
  documents: DocItem[];
}

interface DocsManifest {
  sections: DocSection[];
  defaultDocument?: string;
}

const props = defineProps<{
  baseUrl?: string;
}>();

const route = useRoute();
const currentPath = computed(() => {
  const path = route.params.docPath as string || '';
  return path || (manifest.value?.defaultDocument || 'README.md');
});

const sidebarVisible = ref(true);
const documentTitle = ref('');
const manifest = ref<DocsManifest | null>(null);
const expandedSections = ref<string[]>([]);
const loadingManifest = ref(true);
const manifestError = ref<string | null>(null);

const docSections = computed(() => {
  return manifest.value?.sections || [];
});

// Toggle a section's expanded state
const toggleSection = (sectionId: string) => {
  const index = expandedSections.value.indexOf(sectionId);
  if (index === -1) {
    expandedSections.value.push(sectionId);
  } else {
    expandedSections.value.splice(index, 1);
  }
};

// Handle document loaded event from DocViewer
const onDocLoaded = (path: string) => {
  // Set page title from the first h1 in the document if available
  const h1 = document.querySelector('.doc-content h1');
  if (h1) {
    documentTitle.value = h1.textContent || '';
  } else {
    // Try to find the document title in the manifest
    const allDocs = docSections.value.flatMap(section => section.documents);
    const doc = allDocs.find(d => d.path === path);
    documentTitle.value = doc?.title || path;
  }
};

// Fetch the docs manifest
const fetchManifest = async () => {
  loadingManifest.value = true;
  manifestError.value = null;
  
  try {
    const baseUrl = props.baseUrl || '';
    const response = await fetch(`${baseUrl}/docs/docs-manifest.json`);
    
    if (!response.ok) {
      throw new Error(`Failed to load docs manifest: ${response.status} ${response.statusText}`);
    }
    
    manifest.value = await response.json();
    
    // Expand the section containing the current document
    if (currentPath.value) {
      const sectionWithCurrentDoc = docSections.value.find(section => 
        section.documents.some(doc => doc.path === currentPath.value)
      );
      
      if (sectionWithCurrentDoc) {
        expandedSections.value.push(sectionWithCurrentDoc.id);
      }
    }
  } catch (err) {
    console.error('Error loading docs manifest:', err);
    manifestError.value = err instanceof Error ? err.message : String(err);
    
    // Fallback: create a basic manifest with a single section
    manifest.value = {
      sections: [
        {
          id: 'main',
          title: 'Documentation',
          documents: [
            { path: 'README.md', title: 'README' },
            { path: 'docs/system/AGENT_ARCHITECTURE.md', title: 'Agent Architecture' },
            { path: 'docs/visualization/ANIMATION_OVERVIEW.md', title: 'Animation Overview' },
            { path: 'docs/visualization/government/GOV_ANIMATION_PLAN.md', title: 'Government Animation Plan' },
            { path: 'docs/visualization/MFE_INTEGRATION_PLAN.md', title: 'MFE Integration Plan' }
          ]
        }
      ],
      defaultDocument: 'README.md'
    };
    
    // Expand the fallback section
    expandedSections.value = ['main'];
  } finally {
    loadingManifest.value = false;
  }
};

// Watch for route changes to handle document loading
watch(() => route.params.docPath, () => {
  // Close sidebar on mobile when navigating
  if (window.innerWidth < 768) {
    sidebarVisible.value = false;
  }
});

onMounted(() => {
  fetchManifest();
  
  // Handle responsive sidebar
  const handleResize = () => {
    sidebarVisible.value = window.innerWidth >= 768;
  };
  
  window.addEventListener('resize', handleResize);
  handleResize(); // Set initial state
  
  return () => {
    window.removeEventListener('resize', handleResize);
  };
});
</script>

<style>
.hms-docs-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  height: 100%;
  background-color: #f8f9fa;
  border-right: 1px solid #dee2e6;
  overflow-y: auto;
  position: relative;
  z-index: 10;
  transition: transform 0.3s ease;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  height: 50px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  border-bottom: 1px solid #dee2e6;
  background-color: #ffffff;
}

.document-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.doc-nav {
  padding: 1rem 0;
}

.nav-section {
  margin-bottom: 0.5rem;
}

.section-header {
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.section-header:hover {
  background-color: #e9ecef;
}

.section-icon {
  margin-right: 0.5rem;
  font-size: 0.8rem;
}

.doc-list {
  list-style: none;
  padding: 0;
  margin: 0 0 0 1.5rem;
}

.doc-list li {
  margin: 0.25rem 0;
}

.doc-list a {
  display: block;
  padding: 0.25rem 0.5rem;
  text-decoration: none;
  color: #495057;
  border-radius: 4px;
}

.doc-list a:hover {
  background-color: #e9ecef;
}

.doc-list a.active {
  background-color: #e9ecef;
  font-weight: 500;
  color: #000;
}

.loading-message, .error-message {
  padding: 1rem;
}

.error-message {
  color: #dc3545;
}

.sidebar-toggle {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  margin-right: 0.5rem;
}

.document-path {
  font-weight: 500;
}

/* Animation for section expand/collapse */
.slide-enter-active,
.slide-leave-active {
  transition: max-height 0.3s ease, opacity 0.3s ease;
  max-height: 1000px;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    transform: translateX(-100%);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .sidebar.visible {
    transform: translateX(0);
  }
  
  .desktop-hidden {
    display: block;
  }
  
  .mobile-only {
    display: block;
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
  }
}

@media (min-width: 768px) {
  .desktop-hidden {
    display: none;
  }
  
  .mobile-only {
    display: none;
  }
}
</style> 