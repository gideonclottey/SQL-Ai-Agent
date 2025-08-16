import { useState, useEffect } from 'react'

export default function Settings(){
  const [key, setKey] = useState('')
  useEffect(()=>{ setKey(localStorage.getItem('GEMINI_API_KEY') || '') },[])
  return (
    <div className="max-w-xl mx-auto bg-white rounded-2xl shadow p-6">
      <h1 className="text-xl font-semibold mb-4">Settings</h1>
      <label className="text-sm text-gray-600">Gemini API Key</label>
      <input className="border rounded px-3 py-2 w-full" value={key} onChange={e=>setKey(e.target.value)} placeholder="Paste your Gemini API key" />
      <p className="text-xs text-gray-500 my-2">Stored in your browser (localStorage). It will be sent as an <code>X-Api-Key</code> header to the backend for each chat request.</p>
      <button className="mt-3 bg-black text-white rounded px-4 py-2" onClick={()=>{ localStorage.setItem('GEMINI_API_KEY', key); alert('Saved!') }}>Save</button>
    </div>
  )
}