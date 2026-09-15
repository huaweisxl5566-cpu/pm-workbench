import { defineStore } from 'pinia'
import { ref } from 'vue'
import { notesApi, type Note } from '@/api'

export const useNoteStore = defineStore('notes', () => {
  const notes = ref<Note[]>([])
  const loading = ref(false)
  const search = ref('')
  const categoryFilter = ref('')

  async function fetchNotes() {
    loading.value = true
    try {
      const { data } = await notesApi.list({
        category: categoryFilter.value || undefined,
        search: search.value || undefined,
      })
      notes.value = data
    } finally {
      loading.value = false
    }
  }

  async function addNote(note: Partial<Note>) {
    const { data } = await notesApi.create(note)
    notes.value.unshift(data)
  }

  async function updateNote(id: number, updates: Partial<Note>) {
    const { data } = await notesApi.update(id, updates)
    const idx = notes.value.findIndex(n => n.id === id)
    if (idx !== -1) notes.value[idx] = data
  }

  async function removeNote(id: number) {
    await notesApi.delete(id)
    notes.value = notes.value.filter(n => n.id !== id)
  }

  return { notes, loading, search, categoryFilter, fetchNotes, addNote, updateNote, removeNote }
})
