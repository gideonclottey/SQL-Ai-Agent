import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../lib/api'

export default function Register() {
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState('')

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setErr('')
    try {
      const res = await apiFetch('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) })
      localStorage.setItem('token', res.access_token)
      nav('/chat')
    } catch (e:any) {
      setErr(e.message)
    }
  }

  return (
    <div className="max-w-md mx-auto bg-white rounded-2xl shadow p-6 mt-10">
      <h1 className="text-xl font-semibold mb-4">Create account</h1>
      {err && <div className="bg-red-50 text-red-700 p-2 rounded mb-3">{err}</div>}
      <form onSubmit={submit} className="flex flex-col gap-3">
        <input className="border rounded px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="border rounded px-3 py-2" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="bg-black text-white rounded px-4 py-2">Register</button>
        <div className="text-sm">Have an account? <Link className="text-blue-600" to="/login">Login</Link></div>
      </form>
    </div>
  )
}