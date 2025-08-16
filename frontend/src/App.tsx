import { Route, Routes, Navigate, Link } from 'react-router-dom'
import Login from './pages/Login.tsx'
import Register from './pages/Register.tsx'
import Chat from './pages/Chat.tsx'
import Settings from './pages/Settings.tsx'

function isAuthed() {
  return !!localStorage.getItem('token')
}

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-semibold">AI Agent</Link>
        <nav className="flex gap-4">
          <Link to="/chat">Chat</Link>
          <Link to="/settings">Settings</Link>
          {isAuthed() ? (
            <button onClick={() => { localStorage.removeItem('token'); location.href='/login' }} className="text-red-600">Logout</button>
          ) : (
            <Link to="/login">Login</Link>
          )}
        </nav>
      </header>
      <main className="flex-1 p-4">
        <Routes>
          <Route path="/" element={<Navigate to="/chat" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/chat" element={isAuthed() ? <Chat /> : <Navigate to="/login" />} />
          <Route path="/settings" element={isAuthed() ? <Settings /> : <Navigate to="/login" />} />
        </Routes>
      </main>
    </div>
  )
}