<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { filesApi, type FileItem } from '@/api'

const files = ref<FileItem[]>([])
const loading = ref(false)
const currentPath = ref('')
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function formatSize(bytes: number) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function getFileIcon(name: string, isDir: boolean) {
  if (isDir) return '📁'
  const ext = name.split('.').pop()?.toLowerCase() || ''
  const iconMap: Record<string, string> = {
    pdf: '📄', doc: '📝', docx: '📝', txt: '📃',
    xls: '📊', xlsx: '📊', csv: '📊',
    ppt: '📑', pptx: '📑',
    jpg: '🖼️', jpeg: '🖼️', png: '🖼️', gif: '🖼️', svg: '🖼️',
    mp4: '🎬', avi: '🎬', mov: '🎬',
    mp3: '🎵', wav: '🎵',
    zip: '📦', rar: '📦', '7z': '📦',
    js: '💻', ts: '💻', py: '💻', java: '💻', html: '💻', css: '💻',
  }
  return iconMap[ext] || '📄'
}

async function fetchFiles() {
  loading.value = true
  try {
    const { data } = await filesApi.list(currentPath.value)
    files.value = data
  } finally {
    loading.value = false
  }
}

function navigateTo(dir: string) {
  currentPath.value = currentPath.value ? `${currentPath.value}/${dir}` : dir
  fetchFiles()
}

function goBack() {
  const parts = currentPath.value.split('/')
  parts.pop()
  currentPath.value = parts.join('/')
  fetchFiles()
}

function openUpload() {
  fileInput.value?.click()
}

async function handleUpload(event: Event) {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return
  uploading.value = true
  try {
    for (const file of input.files) {
      await filesApi.upload(file, currentPath.value)
    }
    await fetchFiles()
  } finally {
    uploading.value = false
    input.value = ''
  }
}

async function deleteItem(item: FileItem) {
  const path = currentPath.value ? `${currentPath.value}/${item.name}` : item.name
  if (confirm(`确定要删除 ${item.name} 吗？`)) {
    await filesApi.delete(path)
    await fetchFiles()
  }
}

onMounted(fetchFiles)
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">文件管理</h1>
        <div class="flex items-center gap-1 mt-1 text-sm text-gray-500">
          <button @click="currentPath = ''; fetchFiles()" class="hover:text-primary-600">根目录</button>
          <template v-if="currentPath">
            <span v-for="(part, i) in currentPath.split('/')" :key="i">
              / <button
                @click="currentPath = currentPath.split('/').slice(0, i + 1).join('/'); fetchFiles()"
                class="hover:text-primary-600"
              >{{ part }}</button>
            </span>
          </template>
        </div>
      </div>
      <div class="flex gap-2">
        <button @click="goBack" :disabled="!currentPath" class="btn-secondary disabled:opacity-50">
          ← 返回上级
        </button>
        <button @click="openUpload" class="btn-primary" :disabled="uploading">
          {{ uploading ? '上传中...' : '📤 上传文件' }}
        </button>
        <input ref="fileInput" type="file" multiple @change="handleUpload" class="hidden" />
      </div>
    </div>

    <!-- File List -->
    <div v-if="loading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="files.length === 0" class="card text-center py-12">
      <div class="text-5xl mb-3">📂</div>
      <div class="text-gray-500">此目录为空</div>
    </div>

    <div v-else class="card overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-100">
            <th class="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">名称</th>
            <th class="text-right px-4 py-3 text-xs font-medium text-gray-500 uppercase hidden sm:table-cell">大小</th>
            <th class="text-right px-4 py-3 text-xs font-medium text-gray-500 uppercase hidden md:table-cell">修改时间</th>
            <th class="text-right px-4 py-3 text-xs font-medium text-gray-500 uppercase">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="file in files"
            :key="file.name"
            class="border-b border-gray-50 last:border-0 hover:bg-gray-50 transition-colors"
          >
            <td class="px-4 py-3">
              <button
                @click="file.is_dir ? navigateTo(file.name) : null"
                class="flex items-center gap-3 text-left"
              >
                <span class="text-xl">{{ getFileIcon(file.name, file.is_dir) }}</span>
                <span class="text-sm font-medium text-gray-900" :class="file.is_dir && 'text-primary-600 hover:underline'">
                  {{ file.name }}
                </span>
              </button>
            </td>
            <td class="px-4 py-3 text-right text-sm text-gray-500 hidden sm:table-cell">
              {{ file.is_dir ? '-' : formatSize(file.size) }}
            </td>
            <td class="px-4 py-3 text-right text-sm text-gray-500 hidden md:table-cell">
              {{ formatDate(file.modified) }}
            </td>
            <td class="px-4 py-3 text-right">
              <button @click="deleteItem(file)" class="btn-icon text-red-500 hover:text-red-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
