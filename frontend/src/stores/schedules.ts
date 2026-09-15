import { defineStore } from 'pinia'
import { ref } from 'vue'
import { schedulesApi, type Schedule } from '@/api'

export const useScheduleStore = defineStore('schedules', () => {
  const schedules = ref<Schedule[]>([])
  const loading = ref(false)

  async function fetchSchedules(start?: string, end?: string) {
    loading.value = true
    try {
      const { data } = await schedulesApi.list({ start, end })
      schedules.value = data
    } finally {
      loading.value = false
    }
  }

  async function addSchedule(schedule: Partial<Schedule>) {
    const { data } = await schedulesApi.create(schedule)
    schedules.value.push(data)
  }

  async function updateSchedule(id: number, updates: Partial<Schedule>) {
    const { data } = await schedulesApi.update(id, updates)
    const idx = schedules.value.findIndex(s => s.id === id)
    if (idx !== -1) schedules.value[idx] = data
  }

  async function removeSchedule(id: number) {
    await schedulesApi.delete(id)
    schedules.value = schedules.value.filter(s => s.id !== id)
  }

  return { schedules, loading, fetchSchedules, addSchedule, updateSchedule, removeSchedule }
})
