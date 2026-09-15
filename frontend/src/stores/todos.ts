import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { todosApi, type Todo } from '@/api'

export const useTodoStore = defineStore('todos', () => {
  const todos = ref<Todo[]>([])
  const loading = ref(false)
  const filter = ref<'all' | 'pending' | 'completed'>('all')
  const categoryFilter = ref<string>('')

  const filteredTodos = computed(() => {
    let result = todos.value
    if (filter.value === 'pending') result = result.filter(t => !t.completed)
    if (filter.value === 'completed') result = result.filter(t => t.completed)
    if (categoryFilter.value) result = result.filter(t => t.category === categoryFilter.value)
    return result
  })

  const stats = computed(() => ({
    total: todos.value.length,
    pending: todos.value.filter(t => !t.completed).length,
    completed: todos.value.filter(t => t.completed).length,
    overdue: todos.value.filter(t => !t.completed && t.due_date && new Date(t.due_date) < new Date()).length,
  }))

  async function fetchTodos() {
    loading.value = true
    try {
      const { data } = await todosApi.list()
      todos.value = data
    } finally {
      loading.value = false
    }
  }

  async function addTodo(todo: Partial<Todo>) {
    const { data } = await todosApi.create(todo)
    todos.value.unshift(data)
  }

  async function updateTodo(id: number, updates: Partial<Todo>) {
    const { data } = await todosApi.update(id, updates)
    const idx = todos.value.findIndex(t => t.id === id)
    if (idx !== -1) todos.value[idx] = data
  }

  async function toggleTodo(id: number) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      await updateTodo(id, { completed: !todo.completed })
    }
  }

  async function removeTodo(id: number) {
    await todosApi.delete(id)
    todos.value = todos.value.filter(t => t.id !== id)
  }

  return { todos, loading, filter, categoryFilter, filteredTodos, stats, fetchTodos, addTodo, updateTodo, toggleTodo, removeTodo }
})
