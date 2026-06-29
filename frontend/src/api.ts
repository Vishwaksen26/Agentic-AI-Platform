const apiBase = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'
const wsBase = import.meta.env.VITE_WS_URL ?? 'ws://localhost:8000'

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }

  return response.json() as Promise<T>
}

export function getJson<T>(path: string): Promise<T> {
  return requestJson<T>(path)
}

export function postJson<T>(path: string, body?: unknown): Promise<T> {
  return requestJson<T>(path, {
    method: 'POST',
    body: body === undefined ? undefined : JSON.stringify(body),
  })
}

export function patchJson<T>(path: string, body?: unknown): Promise<T> {
  return requestJson<T>(path, {
    method: 'PATCH',
    body: body === undefined ? undefined : JSON.stringify(body),
  })
}

export function getWebSocketUrl(path: string): string {
  return `${wsBase}${path}`
}