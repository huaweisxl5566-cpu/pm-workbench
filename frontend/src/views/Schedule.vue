<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useScheduleStore } from '@/stores/schedules'
import type { Schedule } from '@/api'

const store = useScheduleStore()
const showAddModal = ref(false)
const editingSchedule = ref<Schedule | null>(null)
const currentDate = ref(new Date())
const viewMode = ref<'week' | 'month'>('week')

const newSchedule = ref({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  all_day: false,
  color: '#4F46E5',
  location: '',
})

const colors = [
  '#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4'
]

const weekDays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

const weekDates = computed(() => {
  const start = new Date(currentDate.value)
  const day = start.getDay()
  start.setDate(start.getDate() - (day === 0 ? 6 : day - 1))
  const dates = []
  for (let i = 0; i < 7; i++) {
    const d = new Date(start)
    d.setDate(d.getDate() + i)
    dates.push(d)
  }
  return dates
})

function formatDate(date: Date) {
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

function formatTime(dateStr: string) {
  return new Date(dateStr).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function isToday(date: Date) {
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

function getSchedulesForDate(date: Date) {
  return store.schedules.filter(s => {
    const start = new Date(s.start_time)
    return start.toDateString() === date.toDateString()
  })
}

function prevWeek() {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() - 7)
  currentDate.value = d
}

function nextWeek() {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() + 7)
  currentDate.value = d
}

function goToday() {
  currentDate.value = new Date()
}

function toInputDatetime(date: Date) {
  return date.toISOString().slice(0, 16)
}

async function handleAdd() {
  if (!newSchedule.value.title.trim() || !newSchedule.value.start_time || !newSchedule.value.end_time) return
  await store.addSchedule(newSchedule.value)
  resetForm()
  showAddModal.value = false
}

function startEdit(schedule: Schedule) {
  editingSchedule.value = schedule
  newSchedule.value = {
    title: schedule.title,
    description: schedule.description,
    start_time: schedule.start_time.slice(0, 16),
    end_time: schedule.end_time.slice(0, 16),
    all_day: schedule.all_day,
    color: schedule.color,
    location: schedule.location,
  }
  showAddModal.value = true
}

async function handleEdit() {
  if (!editingSchedule.value) return
  await store.updateSchedule(editingSchedule.value.id, newSchedule.value)
  resetForm()
  showAddModal.value = false
}

function resetForm() {
  editingSchedule.value = null
  newSchedule.value = { title: '', description: '', start_time: '', end_time: '', all_day: false, color: '#4F46E5', location: '' }
}

function closeModal() {
  showAddModal.value = false
  resetForm()
}

onMounted(() => {
  const start = weekDates.value[0].toISOString()
  const end = weekDates.value[6].toISOString()
  store.fetchSchedules(start, end)
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">日程管理</h1>
        <p class="text-sm text-gray-500 mt-1">本周日程一览</p>
      </div>
      <button @click="showAddModal = true" class="btn-primary">
        + 新建日程
      </button>
    </div>

    <!-- Calendar Navigation -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <button @click="prevWeek" class="btn-icon">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <span class="text-sm font-medium text-gray-900">
          {{ formatDate(weekDates[0]) }} - {{ formatDate(weekDates[6]) }}
        </span>
        <button @click="nextWeek" class="btn-icon">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
        <button @click="goToday" class="btn-secondary text-sm py-1">今天</button>
      </div>
    </div>

    <!-- Week View -->
    <div class="grid grid-cols-7 gap-1 bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div
        v-for="(date, i) in weekDates"
        :key="i"
        class="min-h-[200px] border-r border-gray-100 last:border-r-0"
      >
        <div
          :class="[
            'p-2 text-center border-b border-gray-100',
            isToday(date) ? 'bg-primary-50' : 'bg-gray-50'
          ]"
        >
          <div class="text-xs text-gray-500">{{ weekDays[i] }}</div>
          <div :class="['text-lg font-semibold', isToday(date) ? 'text-primary-600' : 'text-gray-900']">
            {{ date.getDate() }}
          </div>
        </div>
        <div class="p-1 space-y-1">
          <div
            v-for="schedule in getSchedulesForDate(date)"
            :key="schedule.id"
            @click="startEdit(schedule)"
            class="px-2 py-1 rounded text-xs cursor-pointer hover:opacity-80 transition-opacity text-white truncate"
            :style="{ backgroundColor: schedule.color }"
          >
            {{ schedule.title }}
          </div>
        </div>
      </div>
    </div>

    <!-- Upcoming List (mobile) -->
    <div class="lg:hidden card">
      <h2 class="font-semibold text-gray-900 mb-3">近期日程</h2>
      <div v-if="store.schedules.length === 0" class="text-center py-6 text-gray-400">暂无日程</div>
      <div v-else class="space-y-2">
        <div
          v-for="s in store.schedules.slice(0, 5)"
          :key="s.id"
          class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50"
        >
          <div class="w-2 h-8 rounded-full" :style="{ backgroundColor: s.color }"></div>
          <div class="flex-1">
            <div class="text-sm font-medium text-gray-900">{{ s.title }}</div>
            <div class="text-xs text-gray-500">{{ formatDate(new Date(s.start_time)) }} {{ formatTime(s.start_time) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          {{ editingSchedule ? '编辑日程' : '新建日程' }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">标题 *</label>
            <input v-model="newSchedule.title" class="input" placeholder="日程标题" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <textarea v-model="newSchedule.description" class="input" rows="2" placeholder="添加描述..."></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">开始时间 *</label>
              <input v-model="newSchedule.start_time" type="datetime-local" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">结束时间 *</label>
              <input v-model="newSchedule.end_time" type="datetime-local" class="input" />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">地点</label>
            <input v-model="newSchedule.location" class="input" placeholder="添加地点" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">颜色</label>
            <div class="flex gap-2">
              <button
                v-for="c in colors"
                :key="c"
                @click="newSchedule.color = c"
                :class="[
                  'w-8 h-8 rounded-full transition-transform',
                  newSchedule.color === c ? 'ring-2 ring-offset-2 ring-gray-400 scale-110' : ''
                ]"
                :style="{ backgroundColor: c }"
              ></button>
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button @click="closeModal" class="btn-secondary">取消</button>
          <button @click="editingSchedule ? handleEdit() : handleAdd()" class="btn-primary">
            {{ editingSchedule ? '保存' : '创建' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
