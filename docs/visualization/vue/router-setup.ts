import { RouteRecordRaw } from 'vue-router';
import { DocsPage } from './index';

/**
 * Adds the documentation routes to a Vue Router instance
 * 
 * @param baseUrl Optional base URL for API requests (defaults to '')
 * @returns Route configuration object to merge with existing routes
 */
export function setupDocumentationRoutes(baseUrl: string = ''): RouteRecordRaw[] {
  return [
    {
      path: '/docs',
      name: 'docs-root',
      component: DocsPage,
      props: { baseUrl },
      redirect: '/docs/README.md',
    },
    {
      path: '/docs/:docPath(.*)',
      name: 'docs-view',
      component: DocsPage,
      props: route => ({
        baseUrl,
        docPath: route.params.docPath
      })
    }
  ];
}

/**
 * Example usage in main Vue Router setup:
 * 
 * ```ts
 * import { createRouter, createWebHistory } from 'vue-router';
 * import { setupDocumentationRoutes } from '@hms/visualization/vue/router-setup';
 * 
 * const routes = [
 *   // Existing routes
 *   { path: '/', component: Home },
 *   { path: '/dashboard', component: Dashboard },
 *   
 *   // Add documentation routes
 *   ...setupDocumentationRoutes()
 * ];
 * 
 * const router = createRouter({
 *   history: createWebHistory(),
 *   routes
 * });
 * ```
 */ 