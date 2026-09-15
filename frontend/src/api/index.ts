import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export interface Todo {
  id: number
  title: string
  description: string
  completed: boolean
  priority: number
  due_date: string | null
  category: string
  created_at: string
  updated_at: string
}

export interface Note {
  id: number
  title: string
  content: string
  category: string
  pinned: boolean
  created_at: string
  updated_at: string
}

export interface Schedule {
  id: number
  title: string
  description: string
  start_time: string
  end_time: string
  all_day: boolean
  color: string
  location: string
  created_at: string
}

export interface QuickLink {
  id: number
  title: string
  url: string
  icon: string
  category: string
  sort_order: number
  created_at: string
}

export interface Dashboard {
  pending_todos: number
  completed_todos: number
  total_todos: number
  completion_rate: number
  upcoming_events: number
  overdue_todos: number
  total_notes: number
}

export interface Weather {
  city: string
  temp_c: string
  feels_like: string
  humidity: string
  weather_desc: string
  wind_speed: string
  wind_dir: string
}

export interface NewsItem {
  title: string
  url: string
  source: string
}

export interface FileItem {
  name: string
  is_dir: boolean
  size: number
  modified: string
}

// Todos
export const todosApi = {
  list: (params?: { completed?: boolean; category?: string }) =>
    api.get<Todo[]>('/todos', { params }),
  create: (data: Partial<Todo>) => api.post<Todo>('/todos', data),
  update: (id: number, data: Partial<Todo>) => api.put<Todo>(`/todos/${id}`, data),
  delete: (id: number) => api.delete(`/todos/${id}`),
}

// Notes
export const notesApi = {
  list: (params?: { category?: string; search?: string }) =>
    api.get<Note[]>('/notes', { params }),
  create: (data: Partial<Note>) => api.post<Note>('/notes', data),
  update: (id: number, data: Partial<Note>) => api.put<Note>(`/notes/${id}`, data),
  delete: (id: number) => api.delete(`/notes/${id}`),
}

// Schedules
export const schedulesApi = {
  list: (params?: { start?: string; end?: string }) =>
    api.get<Schedule[]>('/schedules', { params }),
  create: (data: Partial<Schedule>) => api.post<Schedule>('/schedules', data),
  update: (id: number, data: Partial<Schedule>) => api.put<Schedule>(`/schedules/${id}`, data),
  delete: (id: number) => api.delete(`/schedules/${id}`),
}

// Quick Links
export const quickLinksApi = {
  list: () => api.get<QuickLink[]>('/quicklinks'),
  create: (data: Partial<QuickLink>) => api.post<QuickLink>('/quicklinks', data),
  update: (id: number, data: Partial<QuickLink>) => api.put<QuickLink>(`/quicklinks/${id}`, data),
  delete: (id: number) => api.delete(`/quicklinks/${id}`),
}

// Dashboard
export const dashboardApi = {
  get: () => api.get<Dashboard>('/dashboard'),
}

// Weather
export const weatherApi = {
  get: (city: string = 'Beijing') => api.get<Weather>('/weather', { params: { city } }),
}

// News
export const newsApi = {
  get: (count: number = 6) => api.get<NewsItem[]>('/news', { params: { count } }),
}

// Files
export const filesApi = {
  list: (path: string = '') => api.get<FileItem[]>('/files', { params: { path } }),
  upload: (file: File, path: string = '') => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/files/upload', formData, { params: { path } })
  },
  delete: (path: string) => api.delete('/files', { params: { path } }),
}

export default api
