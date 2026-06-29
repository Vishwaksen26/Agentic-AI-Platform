import axios, { AxiosError, AxiosInstance, AxiosResponse } from 'axios'
import { ApiError, ApiResponse, PaginationParams, PaginatedResponse } from '../types/common'

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Generic API call handler with error handling
async function apiCall<T>(
  method: 'get' | 'post' | 'put' | 'delete' | 'patch',
  url: string,
  data?: unknown,
  params?: unknown
): Promise<ApiResponse<T>> {
  try {
    const response: AxiosResponse<T> = await apiClient[method](url, data, {
      params,
    })

    return {
      data: response.data,
      status: response.status,
      timestamp: new Date().toISOString(),
    }
  } catch (error) {
    const axiosError = error as AxiosError<{ message?: string; detail?: string }>
    const apiError: ApiError = {
      code: axiosError.code || 'UNKNOWN_ERROR',
      message: axiosError.response?.data?.message || axiosError.message || 'An error occurred',
      statusCode: axiosError.response?.status || 500,
      timestamp: new Date().toISOString(),
      details: axiosError.response?.data,
    }
    throw apiError
  }
}

// API methods
export const api = {
  // Health check
  health: () => apiCall<{ status: string }>('get', '/health'),

  // Workflows
  workflows: {
    list: (params?: PaginationParams) => apiCall<PaginatedResponse<any>>('get', '/workflows', undefined, params),
    get: (id: string) => apiCall<any>('get', `/workflows/${id}`),
    create: (data: unknown) => apiCall<any>('post', '/workflows', data),
    update: (id: string, data: unknown) => apiCall<any>('put', `/workflows/${id}`, data),
    delete: (id: string) => apiCall<void>('delete', `/workflows/${id}`),
  },

  // Agents
  agents: {
    list: () => apiCall<any[]>('get', '/agents'),
    get: (id: string) => apiCall<any>('get', `/agents/${id}`),
  },

  // Approvals
  approvals: {
    list: (params?: PaginationParams) => apiCall<PaginatedResponse<any>>('get', '/approvals', undefined, params),
    get: (id: string) => apiCall<any>('get', `/approvals/${id}`),
    approve: (id: string, data?: unknown) => apiCall<any>('post', `/approvals/${id}/approve`, data),
    reject: (id: string, data?: unknown) => apiCall<any>('post', `/approvals/${id}/reject`, data),
  },

  // Analytics
  analytics: {
    summary: () => apiCall<any>('get', '/analytics/summary'),
    metrics: (params?: PaginationParams) => apiCall<PaginatedResponse<any>>('get', '/analytics/metrics', undefined, params),
  },

  // Demo
  demo: {
    start: (data?: unknown) => apiCall<any>('post', '/demo/start', data),
  },
}

// WebSocket connection
export function createWebSocket(path: string, onMessage: (data: unknown) => void, onError?: (error: Event) => void) {
  const wsUrl = import.meta.env.VITE_WS_URL || `ws://localhost:8000`
  const fullUrl = `${wsUrl}${path}`

  const ws = new WebSocket(fullUrl)

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (e) {
      console.error('Failed to parse WebSocket message:', e)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
    onError?.(error)
  }

  return ws
}

export default apiClient
