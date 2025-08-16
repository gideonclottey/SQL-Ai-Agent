import { useState } from 'react'
import ChatMessage from '../components/ChatMessage'
import { apiFetch } from '../lib/api'

interface Msg { role: 'user'|'assistant'; content: string }

export default function Chat(){
  const [messages, setMessages] = useState<Msg[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function send(){
    if(!input.trim()) return
    const newMsgs = [...messages, { role: 'user', content: input }]
    setMessages(newMsgs); setInput(''); setLoading(true); setError('')
    try {
      const res = await apiFetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ message: input, history: newMsgs.slice(-6) })
      })
      setMessages([...newMsgs, { role: 'assistant', content: res.answer }])
    } catch (e:any){
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-2xl shadow p-4 min-h-[60vh]">
        {messages.map((m, i) => <ChatMessage key={i} role={m.role} content={m.content} />)}
        {error && <div className="text-red-600 text-sm">{error}</div>}
      </div>
      <div className="mt-4 flex gap-2">
        <input
          className="border rounded px-3 py-2 flex-1"
          placeholder="Ask the agent…"
          value={input}
          onChange={e=>setInput(e.target.value)}
          onKeyDown={e=>{ if(e.key==='Enter') send() }}
        />
        <button className="bg-black text-white rounded px-4 py-2" onClick={send} disabled={loading}>
          {loading ? 'Thinking…' : 'Send'}
        </button>
      </div>
    </div>
  )
}
