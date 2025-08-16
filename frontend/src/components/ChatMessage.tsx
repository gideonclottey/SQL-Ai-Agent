export default function ChatMessage({ role, content }: { role: 'user'|'assistant', content: string }) {
  const isUser = role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
      <div className={`max-w-[75%] rounded-2xl px-4 py-2 shadow ${isUser ? 'bg-blue-100' : 'bg-white'}`}>
        <div className="text-sm text-gray-700 whitespace-pre-wrap">{content}</div>
      </div>
    </div>
  )
}