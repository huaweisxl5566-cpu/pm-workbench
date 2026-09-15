<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useTodoStore } from '@/stores/todos'
import type { Todo } from '@/api'

const store = useTodoStore()
const showAddModal = ref(false)
const editingTodo = ref<Todo | null>(null)
const newTodo = ref({
  title: '',
  description: '',
  priority: 0,
  due_date: null as string | null,
  category: 'general',
})

const categories = ['general', 'work', 'personal', 'meeting', 'review']
const priorities = [
  { value: 0, label: '普通', class: 'badge-blue' },
  { value: 1, label: '低', class: 'badge-blue' },
  { value: 2, label: '重要', class: 'badge-yellow' },
  { value: 3, label: '紧急', class: 'badge-red' },
]

function getPriorityBadge(priority: number) {
  return priorities.find(p => p.value === priority) || priorities[0]
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

function isOverdue(todo: Todo) {
  return !todo.completed && todo.due_date && new Date(todo.due_date) < new Date()
}

async function handleAdd() {
  if (!newTodo.value.title.trim()) return
  await store.addTodo(newTodo.value)
  newTodo.value = { title: '', description: '', priority: 0, due_date: null, category: 'general' }
  showAddModal.value = false
}

function startEdit(todo: Todo) {
  editingTodo.value = todo
  newTodo.value = {
    title: todo.title,
    description: todo.description,
    priority: todo.priority,
    due_date: todo.due_date || null,
    category: todo.category,
  }
  showAddModal.value = true
}

async function handleEdit() {
  if (!editingTodo.value || !newTodo.value.title.trim()) return
  await store.updateTodo(editingTodo.value.id, newTodo.value)
  editingTodo.value = null
  newTodo.value = { title: '', description: '', priority: 0, due_date: null, category: 'general' }
  showAddModal.value = false
}

function closeModal() {
  showAddModal.value = false
  editingTodo.value = null
  newTodo.value = { title: '', description: '', priority: 0, due_date: null, category: 'general' }
}

onMounted(() => {
  store.fetchTodos()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">待办事项</h1>
        <p class="text-sm text-gray-500 mt-1">
          {{ store.stats.pending }} 待处理 · {{ store.stats.completed }} 已完成
          <span v-if="store.stats.overdue" class="text-red-500"> · {{ store.stats.overdue }} 已过期</span>
        </p>
      </div>
      <button @click="showAddModal = true" class="btn-primary">
        + 新建待办
      </button>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-2">
      <button
        v-for="f in ['all', 'pending', 'completed'] as const"
        :key="f"
        @click="store.filter = f"
        :class="[
          'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
          store.filter === f ? 'bg-primary-100 text-primary-700' : 'bg-white text-gray-600 hover:bg-gray-100'
        ]"
      >
        {{ f === 'all' ? '全部' : f === 'pending' ? '待处理' : '已完成' }}
      </button>
      <div class="w-px bg-gray-200 mx-1"></div>
      <select
        v-model="store.categoryFilter"
        @change="store.fetchTodos()"
        class="input w-auto"
      >
        <option value="">所有分类</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <!-- Todo List -->
    <div v-if="store.loading" class="flex items-center justify-center h-32">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="store.filteredTodos.length === 0" class="card text-center py-12">
      <div class="text-5xl mb-3">🎉</div>
      <div class="text-gray-500">没有待办事项</div>
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="todo in store.filteredTodos"
        :key="todo.id"
        :class="[
          'card flex items-center gap-4 group',
          isOverdue(todo) && 'border-red-200 bg-red-50/50'
        ]"
      >
        <button
          @click="store.toggleTodo(todo.id)"
          :class="[
            'w-5 h-5 rounded-full border-2 flex-shrink-0 transition-colors flex items-center justify-center',
            todo.completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-primary-400'
          ]"
        >
          <svg v-if="todo.completed" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </button>

        <div class="flex-1 min-w-0">
          <div class="text-sm font-medium text-gray-900 truncate" :class="todo.completed && 'line-through text-gray-400'">
            {{ todo.title }}
          </div>
          <div v-if="todo.description" class="text-xs text-gray-500 truncate mt-0.5">
            {{ todo.description }}
          </div>
          <div class="flex items-center gap-2 mt-1">
            <span :class="['badge text-xs', getPriorityBadge(todo.priority).class]">
              {{ getPriorityBadge(todo.priority).label }}
            </span>
            <span v-if="todo.due_date" class="text-xs" :class="isOverdue(todo) ? 'text-red-500' : 'text-gray-500'">
              📅 {{ formatDate(todo.due_date) }}
            </span>
            <span class="text-xs text-gray-400">{{ todo.category }}</span>
          </div>
        </div>

        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button @click="startEdit(todo)" class="btn-icon">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button @click="store.removeTodo(todo.id)" class="btn-icon text-red-500 hover:text-red-600">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ editingTodo ? '编辑待办' : '新建待办' }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">标题 *</label>
            <input v-model="newTodo.title" class="input" placeholder="输入待办标题" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <textarea v-model="newTodo.description" class="input" rows="3" placeholder="添加描述..."></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">优先级</label>
              <select v-model="newTodo.priority" class="input">
                <option v-for="p in priorities" :key="p.value" :value="p.value">{{ p.label }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">截止日期</label>
              <input v-model="newTodo.due_date" type="date" class="input" />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
            <select v-model="newTodo.category" class="input">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button @click="closeModal" class="btn-secondary">取消</button>
          <button @click="editingTodo ? handleEdit() : handleAdd()" class="btn-primary">
            {{ editingTodo ? '保存' : '创建' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
