import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/views/Dashboard.vue'),
    },
    {
      path: '/todos',
      name: 'todos',
      component: () => import('@/views/Todos.vue'),
    },
    {
      path: '/notes',
      name: 'notes',
      component: () => import('@/views/Notes.vue'),
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: () => import('@/views/Schedule.vue'),
    },
    {
      path: '/files',
      name: 'files',
      component: () => import('@/views/Files.vue'),
    },
    {
      path: '/shortcuts',
      name: 'shortcuts',
      component: () => import('@/views/Shortcuts.vue'),
    },
  ],
})

export default router
