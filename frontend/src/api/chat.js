import api from './index'

// SSE 流式对话
export function chatStream(sessionId, userId, query) {
  return fetch(`/chat/${sessionId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, query })
  })
}

// 获取会话历史
export function getHistory(sessionId, limit = 20) {
  return api.get(`/chat/${sessionId}/history`, { params: { limit } })
}
