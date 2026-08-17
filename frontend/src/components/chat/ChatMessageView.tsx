import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { ChatMessage } from '../../api/client'

interface Props {
  message: ChatMessage
  streaming?: boolean
}

/**
 * Rendert eine Chat-Nachricht. Assistenten-Antworten als Markdown (Überschriften,
 * Listen, Tabellen — nötig für Berichtsentwürfe); Nutzer-Nachrichten als Klartext
 * mit erhaltenen Zeilenumbrüchen.
 */
export default function ChatMessageView({ message, streaming }: Props) {
  const isUser = message.role === 'user'
  return (
    <div className={`chat-msg ${isUser ? 'chat-msg-user' : 'chat-msg-assistant'}`}>
      {isUser ? (
        <span style={{ whiteSpace: 'pre-wrap' }}>{message.content}</span>
      ) : (
        <div className="chat-markdown">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content || ''}</ReactMarkdown>
          {streaming && <span className="chat-cursor">▍</span>}
        </div>
      )}
    </div>
  )
}
