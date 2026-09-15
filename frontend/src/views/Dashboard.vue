<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dashboardApi, weatherApi, newsApi, todosApi, schedulesApi, type Dashboard, type Weather, type NewsItem, type Todo, type Schedule } from '@/api'

const dashboard = ref<Dashboard | null>(null)
const weather = ref<Weather | null>(null)
const news = ref<NewsItem[]>([])
const upcomingTodos = ref<Todo[]>([])
const upcomingSchedules = ref<Schedule[]>([])
const loading = ref(true)
const currentTime = ref(new Date())

function updateTime() {
  currentTime.value = new Date()
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

function formatTime(dateStr: string) {
  return new Date(dateStr).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function getGreeting() {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  return '晚上好'
}

onMounted(async () => {
  setInterval(updateTime, 1000)
  try {
    const [dashRes, weatherRes, newsRes, todosRes, schedulesRes] = await Promise.all([
      dashboardApi.get(),
      weatherApi.get(),
      newsApi.get(5),
      todosApi.list({ completed: false }),
      schedulesApi.list(),
    ])
    dashboard.value = dashRes.data
    weather.value = weatherRes.data
    news.value = newsRes.data
    upcomingTodos.value = todosRes.data.slice(0, 5)
    const now = new Date()
    const weekEnd = new Date(now)
    weekEnd.setDate(weekEnd.getDate() + 7)
    upcomingSchedules.value = schedulesRes.data
      .filter(s => new Date(s.start_time) >= now && new Date(s.start_time) <= weekEnd)
      .slice(0, 5)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div v-if="loading" class="flex items-center justify-center h-64">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
  </div>

  <div v-else class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ getGreeting() }}，项目经理</h1>
        <p class="text-sm text-gray-500 mt-1">
          {{ currentTime.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }) }}
          {{ currentTime.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) }}
        </p>
      </div>
      <!-- Weather Card -->
      <div v-if="weather" class="card flex items-center gap-4">
        <div class="text-3xl">🌤️</div>
        <div>
          <div class="text-2xl font-bold text-gray-900">{{ weather.temp_c }}°C</div>
          <div class="text-sm text-gray-500">{{ weather.weather_desc }} · {{ weather.city }}</div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-primary-100 flex items-center justify-center text-xl">📋</div>
          <div>
            <div class="text-2xl font-bold text-gray-900">{{ dashboard?.pending_todos || 0 }}</div>
            <div class="text-xs text-gray-500">待办事项</div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center text-xl">✅</div>
          <div>
            <div class="text-2xl font-bold text-gray-900">{{ dashboard?.completed_todos || 0 }}</div>
            <div class="text-xs text-gray-500">已完成</div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-yellow-100 flex items-center justify-center text-xl">📅</div>
          <div>
            <div class="text-2xl font-bold text-gray-900">{{ dashboard?.upcoming_events || 0 }}</div>
            <div class="text-xs text-gray-500">本周日程</div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg" :class="dashboard?.overdue_todos ? 'bg-red-100' : 'bg-gray-100'">
            <div class="flex items-center justify-center h-full text-xl">⏰</div>
          </div>
          <div>
            <div class="text-2xl font-bold" :class="dashboard?.overdue_todos ? 'text-red-600' : 'text-gray-900'">
              {{ dashboard?.overdue_todos || 0 }}
            </div>
            <div class="text-xs text-gray-500">已过期</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid lg:grid-cols-3 gap-6">
      <!-- Upcoming Todos -->
      <div class="lg:col-span-2 card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-semibold text-gray-900">待办事项</h2>
          <router-link to="/todos" class="text-sm text-primary-600 hover:text-primary-700">查看全部</router-link>
        </div>
        <div v-if="upcomingTodos.length === 0" class="text-center py-8 text-gray-400">
          <div class="text-4xl mb-2">🎉</div>
          <div>没有待办事项</div>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="todo in upcomingTodos"
            :key="todo.id"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div
              class="w-5 h-5 rounded-full border-2 cursor-pointer transition-colors flex items-center justify-center"
              :class="todo.completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-primary-400'"
            >
              <svg v-if="todo.completed" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 truncate">{{ todo.title }}</div>
              <div v-if="todo.due_date" class="text-xs text-gray-500 mt-0.5">
                截止: {{ formatDate(todo.due_date) }}
              </div>
            </div>
            <span
              v-if="todo.priority >= 3"
              class="badge badge-red"
            >紧急</span>
            <span
              v-else-if="todo.priority >= 2"
              class="badge badge-yellow"
            >重要</span>
          </div>
        </div>
      </div>

      <!-- Upcoming Schedule -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-semibold text-gray-900">本周日程</h2>
          <router-link to="/schedule" class="text-sm text-primary-600 hover:text-primary-700">查看全部</router-link>
        </div>
        <div v-if="upcomingSchedules.length === 0" class="text-center py-8 text-gray-400">
          <div class="text-4xl mb-2">📭</div>
          <div>暂无日程安排</div>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="schedule in upcomingSchedules"
            :key="schedule.id"
            class="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div class="w-1 h-full min-h-[40px] rounded-full flex-shrink-0" :style="{ backgroundColor: schedule.color }"></div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 truncate">{{ schedule.title }}</div>
              <div class="text-xs text-gray-500 mt-0.5">
                {{ formatDate(schedule.start_time) }} {{ formatTime(schedule.start_time) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- News -->
    <div class="card">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-semibold text-gray-900">📰 新闻资讯</h2>
      </div>
      <div v-if="news.length === 0" class="text-center py-8 text-gray-400">暂无新闻</div>
      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <a
          v-for="item in news"
          :key="item.url"
          :href="item.url"
          target="_blank"
          class="block p-4 rounded-lg border border-gray-100 hover:border-primary-200 hover:bg-primary-50 transition-all duration-200"
        >
          <div class="text-sm font-medium text-gray-900 line-clamp-2">{{ item.title }}</div>
          <div class="text-xs text-gray-500 mt-2">{{ item.source }}</div>
        </a>
      </div>
    </div>
  </div>
</template>
