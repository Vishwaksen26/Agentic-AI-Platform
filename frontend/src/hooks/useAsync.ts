import { useState, useCallback, useEffect } from 'react'
import { useQuery, useMutation, useInfiniteQuery } from '@tanstack/react-query'
import { ApiError } from '../types/common'

// Hook for handling async operations with loading and error states
export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
) {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)

  const execute = useCallback(async () => {
    setStatus('loading')
    setData(null)
    setError(null)

    try {
      const response = await asyncFunction()
      setData(response)
      setStatus('success')
      return response
    } catch (error) {
      setError(error instanceof Error ? error : new Error(String(error)))
      setStatus('error')
      throw error
    }
  }, [asyncFunction])

  useEffect(() => {
    if (immediate) {
      execute()
    }
  }, [execute, immediate])

  return { execute, status, data, error }
}

// Hook for handling API queries with React Query
export function useApiQuery<T>(
  queryKey: string[],
  queryFn: () => Promise<T>,
  options = {}
) {
  return useQuery({
    queryKey,
    queryFn,
    ...options,
  })
}

// Hook for handling API mutations
export function useApiMutation<T, D = unknown>(
  mutationFn: (data: D) => Promise<T>,
  options = {}
) {
  return useMutation({
    mutationFn,
    ...options,
  })
}

// Hook for handling API errors
export function useApiError() {
  const [error, setError] = useState<ApiError | null>(null)

  const handleError = useCallback((err: unknown) => {
    if (err instanceof Error) {
      const apiError: ApiError = {
        code: 'API_ERROR',
        message: err.message,
        statusCode: 500,
        timestamp: new Date().toISOString(),
      }
      setError(apiError)
    } else if (typeof err === 'object' && err !== null && 'message' in err) {
      setError(err as ApiError)
    }
  }, [])

  const clearError = useCallback(() => setError(null), [])

  return { error, handleError, clearError }
}

// Hook for managing pagination
export function usePagination(initialPage = 1, initialLimit = 10) {
  const [page, setPage] = useState(initialPage)
  const [limit, setLimit] = useState(initialLimit)

  const goToPage = useCallback((newPage: number) => {
    setPage(Math.max(1, newPage))
  }, [])

  const nextPage = useCallback(() => {
    setPage((prev) => prev + 1)
  }, [])

  const prevPage = useCallback(() => {
    setPage((prev) => Math.max(1, prev - 1))
  }, [])

  const setPageSize = useCallback((newLimit: number) => {
    setLimit(Math.max(1, newLimit))
    setPage(1) // Reset to first page when changing page size
  }, [])

  return { page, limit, goToPage, nextPage, prevPage, setPageSize }
}

// Hook for form state management
export function useForm<T extends Record<string, unknown>>(
  initialValues: T,
  onSubmit: (values: T) => Promise<void> | void
) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({})
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    setValues((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }))
  }, [])

  const handleBlur = useCallback((e: React.FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name } = e.target
    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }))
  }, [])

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault()
      setIsSubmitting(true)
      try {
        await onSubmit(values)
      } catch (error) {
        console.error('Form submission error:', error)
      } finally {
        setIsSubmitting(false)
      }
    },
    [values, onSubmit]
  )

  const setFieldValue = useCallback((name: keyof T, value: unknown) => {
    setValues((prev) => ({
      ...prev,
      [name]: value,
    }))
  }, [])

  const setFieldError = useCallback((name: keyof T, error: string) => {
    setErrors((prev) => ({
      ...prev,
      [name]: error,
    }))
  }, [])

  const resetForm = useCallback(() => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
  }, [initialValues])

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    setFieldValue,
    setFieldError,
    resetForm,
  }
}

// Hook for local storage
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  const setValue = useCallback(
    (value: T | ((val: T) => T)) => {
      try {
        const valueToStore = value instanceof Function ? value(storedValue) : value
        setStoredValue(valueToStore)
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      } catch (error) {
        console.error(`Error setting localStorage key "${key}":`, error)
      }
    },
    [key, storedValue]
  )

  return [storedValue, setValue] as const
}

// Hook for debounced value
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Hook for previous value
export function usePrevious<T>(value: T): T | undefined {
  const ref = React.useRef<T>()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}
