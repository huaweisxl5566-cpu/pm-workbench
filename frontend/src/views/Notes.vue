<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useNoteStore } from '@/stores/notes'
import type { Note } from '@/api'

const store = useNoteStore()
const showAddModal = ref(false)
const editingNote = ref<Note | null>(null)
const newNote = ref({
  title: '',
  content: '',
  category: 'general',
  pinned: false,
})

const categories = ['general', 'work', 'meeting', 'idea', 'todo']

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function handleAdd() {
  if (!newNote.value.title.trim()) return
  await store.addNote(newNote.value)
  newNote.value = { title: '', content: '', category: 'general', pinned: false }
  showAddModal.value = false
}

function startEdit(note: Note) {
  editingNote.value = note
  newNote.value = {
    title: note.title,
    content: note.content,
    category: note.category,
    pinned: note.pinned,
  }
  showAddModal.value = true
}

async function handleEdit() {
  if (!editingNote.value || !newNote.value.title.trim()) return
  await store.updateNote(editingNote.value.id, newNote.value)
  editingNote.value = null
  newNote.value = { title: '', content: '', category: 'general', pinned: false }
  showAddModal.value = false
}

function togglePin(note: Note) {
  store.updateNote(note.id, { pinned: !note.pinned })
}

function closeModal() {
  showAddModal.value = false
  editingNote.value = null
  newNote.value = { title: '', content: '', category: 'general', pinned: false }
}

let searchTimeout: ReturnType<typeof setTimeout>
function onSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => store.fetchNotes(), 300)
}

onMounted(() => {
  store.fetchNotes()
})

watch(() => store.categoryFilter, () => store.fetchNotes())
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">笔记</h1>
        <p class="text-sm text-gray-500 mt-1">共 {{ store.notes.length }} 条笔记</p>
      </div>
      <button @click="showAddModal = true" class="btn-primary">
        + 新建笔记
      </button>
    </div>

    <!-- Search & Filter -->
    <div class="flex flex-col sm:flex-row gap-3">
      <div class="flex-1 relative">
        <input
          v-model="store.search"
          @input="onSearch"
          class="input pl-10"
          placeholder="搜索笔记..."
        />
        <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <select v-model="store.categoryFilter" class="input w-auto">
        <option value="">所有分类</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <!-- Notes Grid -->
    <div v-if="store.loading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="store.notes.length === 0" class="card text-center py-12">
      <div class="text-5xl mb-3">📝</div>
      <div class="text-gray-500">暂无笔记</div>
    </div>

    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="note in store.notes"
        :key="note.id"
        class="card group relative"
      >
        <div class="absolute top-3 right-3 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button @click="togglePin(note)" class="btn-icon" :class="note.pinned ? 'text-yellow-500' : ''">
            <svg class="w-4 h-4" :fill="note.pinned ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>
          <button @click="startEdit(note)" class="btn-icon">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button @click="store.removeNote(note.id)" class="btn-icon text-red-500">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>

        <div class="mb-2">
          <div class="flex items-center gap-2">
            <span v-if="note.pinned" class="text-yellow-500 text-sm">📌</span>
            <h3 class="font-medium text-gray-900 truncate">{{ note.title }}</h3>
          </div>
          <span class="badge badge-blue text-xs mt-1">{{ note.category }}</span>
        </div>

        <p class="text-sm text-gray-600 line-clamp-4 whitespace-pre-wrap">{{ note.content || '暂无内容' }}</p>

        <div class="mt-3 pt-3 border-t border-gray-100 text-xs text-gray-400">
          {{ formatDate(note.updated_at) }}
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ editingNote ? '编辑笔记' : '新建笔记' }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">标题 *</label>
            <input v-model="newNote.title" class="input" placeholder="输入笔记标题" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">内容</label>
            <textarea v-model="newNote.content" class="input" rows="10" placeholder="开始写笔记..."></textarea>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
              <select v-model="newNote.category" class="input">
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            <div class="flex items-center gap-2 pt-6">
              <input type="checkbox" id="pinned" v-model="newNote.pinned" class="rounded text-primary-600" />
              <label for="pinned" class="text-sm text-gray-700">置顶</label>
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button @click="closeModal" class="btn-secondary">取消</button>
          <button @click="editingNote ? handleEdit() : handleAdd()" class="btn-primary">
            {{ editingNote ? '保存' : '创建' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
