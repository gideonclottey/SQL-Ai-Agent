export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token')
  const apiKey = localStorage.getItem('GEMINI_API_KEY')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers || {} as any),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (apiKey) headers['X-Api-Key'] = apiKey

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}