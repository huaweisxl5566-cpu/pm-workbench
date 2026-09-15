<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)

const navItems = [
  { path: '/', label: '工作台', icon: '📊' },
  { path: '/todos', label: '待办事项', icon: '✅' },
  { path: '/notes', label: '笔记', icon: '📝' },
  { path: '/schedule', label: '日程', icon: '📅' },
  { path: '/files', label: '文件', icon: '📁' },
  { path: '/shortcuts', label: '快捷操作', icon: '⚡' },
]

function navigateTo(path: string) {
  router.push(path)
  mobileMenuOpen.value = false
}

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Sidebar -->
    <aside class="hidden lg:flex lg:flex-col lg:w-64 lg:fixed lg:inset-y-0 bg-white border-r border-gray-200">
      <div class="flex items-center h-16 px-6 border-b border-gray-200">
        <span class="text-2xl mr-3">🎯</span>
        <h1 class="text-lg font-bold text-gray-900">PM Workbench</h1>
      </div>
      <nav class="flex-1 px-3 py-4 space-y-1">
        <button
          v-for="item in navItems"
          :key="item.path"
          @click="navigateTo(item.path)"
          :class="[
            'w-full flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200',
            isActive(item.path)
              ? 'bg-primary-50 text-primary-700'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
          ]"
        >
          <span class="text-lg mr-3">{{ item.icon }}</span>
          {{ item.label }}
        </button>
      </nav>
      <div class="p-4 border-t border-gray-200">
        <div class="text-xs text-gray-400">PM Workbench v1.0</div>
      </div>
    </aside>

    <!-- Mobile Header -->
    <div class="lg:hidden fixed top-0 inset-x-0 z-50 bg-white border-b border-gray-200">
      <div class="flex items-center justify-between h-14 px-4">
        <div class="flex items-center">
          <span class="text-xl mr-2">🎯</span>
          <h1 class="text-base font-bold text-gray-900">PM Workbench</h1>
        </div>
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="btn-icon"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="bg-white border-t border-gray-100">
        <nav class="px-3 py-2">
          <button
            v-for="item in navItems"
            :key="item.path"
            @click="navigateTo(item.path)"
            :class="[
              'w-full flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200',
              isActive(item.path)
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-600 hover:bg-gray-50'
            ]"
          >
            <span class="text-lg mr-3">{{ item.icon }}</span>
            {{ item.label }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <main class="lg:ml-64 min-h-screen pt-14 lg:pt-0">
      <div class="p-4 lg:p-6 max-w-7xl mx-auto">
        <router-view />
      </div>
    </main>
  </div>
</template>
