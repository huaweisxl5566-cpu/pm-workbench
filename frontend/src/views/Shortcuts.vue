<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { quickLinksApi, type QuickLink } from '@/api'

const links = ref<QuickLink[]>([])
const loading = ref(false)
const showAddModal = ref(false)
const editingLink = ref<QuickLink | null>(null)

const newLink = ref({
  title: '',
  url: '',
  icon: '🔗',
  category: 'general',
  sort_order: 0,
})

const icons = ['🔗', '📧', '📊', '📁', '💬', '🎯', '📝', '🔍', '🌐', '⚙️', '📅', '🤖', '📦', '🚀', '💡']
const categories = ['general', 'work', 'dev', 'design', 'docs', 'social']

function startEdit(link: QuickLink) {
  editingLink.value = link
  newLink.value = {
    title: link.title,
    url: link.url,
    icon: link.icon,
    category: link.category,
    sort_order: link.sort_order,
  }
  showAddModal.value = true
}

async function handleAdd() {
  if (!newLink.value.title.trim() || !newLink.value.url.trim()) return
  await quickLinksApi.create(newLink.value)
  resetForm()
  await fetchLinks()
}

async function handleEdit() {
  if (!editingLink.value) return
  await quickLinksApi.update(editingLink.value.id, newLink.value)
  resetForm()
  await fetchLinks()
}

function resetForm() {
  showAddModal.value = false
  editingLink.value = null
  newLink.value = { title: '', url: '', icon: '🔗', category: 'general', sort_order: 0 }
}

async function deleteLink(id: number) {
  if (confirm('确定要删除此快捷链接吗？')) {
    await quickLinksApi.delete(id)
    await fetchLinks()
  }
}

async function fetchLinks() {
  loading.value = true
  try {
    const { data } = await quickLinksApi.list()
    links.value = data
  } finally {
    loading.value = false
  }
}

onMounted(fetchLinks)
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">快捷操作</h1>
        <p class="text-sm text-gray-500 mt-1">常用链接和工具快捷方式</p>
      </div>
      <button @click="showAddModal = true" class="btn-primary">
        + 添加链接
      </button>
    </div>

    <!-- Links Grid -->
    <div v-if="loading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="links.length === 0" class="card text-center py-12">
      <div class="text-5xl mb-3">⚡</div>
      <div class="text-gray-500">暂无快捷链接</div>
      <p class="text-sm text-gray-400 mt-1">点击上方按钮添加常用链接</p>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <a
        v-for="link in links"
        :key="link.id"
        :href="link.url"
        target="_blank"
        rel="noopener noreferrer"
        class="card group relative text-center hover:border-primary-200 hover:bg-primary-50/50"
      >
        <button
          @click.prevent="startEdit(link)"
          class="absolute top-2 right-2 btn-icon opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <button
          @click.prevent="deleteLink(link.id)"
          class="absolute top-2 left-2 btn-icon text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div class="text-3xl mb-2">{{ link.icon }}</div>
        <div class="text-sm font-medium text-gray-900 truncate">{{ link.title }}</div>
        <div class="text-xs text-gray-400 mt-1 truncate">{{ new URL(link.url).hostname }}</div>
      </a>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="resetForm">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ editingLink ? '编辑链接' : '添加链接' }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">名称 *</label>
            <input v-model="newLink.title" class="input" placeholder="链接名称" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">URL *</label>
            <input v-model="newLink.url" class="input" placeholder="https://..." />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">图标</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="icon in icons"
                :key="icon"
                @click="newLink.icon = icon"
                :class="[
                  'w-10 h-10 rounded-lg flex items-center justify-center text-xl transition-all',
                  newLink.icon === icon ? 'bg-primary-100 ring-2 ring-primary-500' : 'bg-gray-100 hover:bg-gray-200'
                ]"
              >
                {{ icon }}
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
            <select v-model="newLink.category" class="input">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button @click="resetForm" class="btn-secondary">取消</button>
          <button @click="editingLink ? handleEdit() : handleAdd()" class="btn-primary">
            {{ editingLink ? '保存' : '添加' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
