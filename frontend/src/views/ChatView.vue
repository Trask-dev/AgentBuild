<template>
  <div class="chat-view">
    <!-- 顶部 -->
    <header class="chat-top">
      <div class="top-left">
        <el-select
          v-model="pickedAgentId"
          placeholder="选择一个智能体开始对话"
          size="large"
          class="agent-pick"
          :teleported="false"
          @change="onPickAgent"
        >
          <el-option v-for="a in store.agents" :key="a.id" :label="a.name" :value="a.id" />
        </el-select>
      </div>
      <div class="top-right">
        <span v-if="store.currentAgent" class="agent-tag">
          {{ store.currentAgent.name }}
        </span>
      </div>
    </header>

    <!-- 消息区 -->
    <div class="msg-area" ref="msgArea">
      <div v-if="msgs.length === 0 && !streaming" class="welcome">
        <div class="welcome-icon"><el-icon :size="40"><ChatLineSquare /></el-icon></div>
        <h2>开始对话</h2>
        <p>选择一个智能体，输入你的问题</p>
      </div>

      <ChatMessage
        v-for="(m,i) in msgs"
        :key="i"
        :role="m.role"
        :content="m.content"
      />

      <!-- 流式打字中 -->
      <div v-if="streaming" class="msg-row assistant">
        <div class="msg-avatar"><el-icon :size="18"><Cpu /></el-icon></div>
        <div class="msg-bubble streaming">
          {{ streamText }}<span class="cursor">|</span>
        </div>
      </div>
    </div>

    <!-- 输入区 -->
    <ChatInput :disabled="!pickedAgentId || streaming" @send="onSend" />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { getAgents } from '../api/agent'
import { createSession } from '../api/session'
import { chatStream, getHistory } from '../api/chat'
import { ElMessage } from 'element-plus'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'

const route = useRoute()
const router = useRouter()
const store = useAppStore()

const pickedAgentId = ref(null)
const msgs = ref([])
const streaming = ref(false)
const streamText = ref('')
const msgArea = ref(null)

// --- 初始化 ---
onMounted(async () => {
  // 加载智能体列表
  try { const r = await getAgents(); store.setAgents(r.data) } catch {}

  // 路由带参数 → 恢复会话
  const { agentId, sessionId } = route.params
  if (agentId && sessionId) {
    pickedAgentId.value = Number(agentId)
    const agent = store.agents.find(a => a.id === pickedAgentId.value)
    if (agent) store.setCurrentAgent(agent)
    await loadHistory(Number(sessionId))
  }

  store.setMenuActive('chat')
})

// --- 加载历史 ---
async function loadHistory(sessionId) {
  try {
    const r = await getHistory(sessionId)
    const list = r.data
    msgs.value = []
    for (const item of list) {
      if (item.user_msg) msgs.value.push({ role: 'user', content: item.user_msg })
      if (item.ai_msg)   msgs.value.push({ role: 'assistant', content: item.ai_msg })
    }
    await scrollBottom()
  } catch {}
}

// --- 选择智能体 ---
function onPickAgent(id) {
  const agent = store.agents.find(a => a.id === id)
  store.setCurrentAgent(agent)
}

// --- 发送消息 ---
async function onSend(text) {
  if (!pickedAgentId.value) return ElMessage.warning('请先选择智能体')

  let sid = store.currentSession?.id

  // 无会话 → 创建
  if (!sid) {
    try {
      const r = await createSession({
        user_id: 1,
        agent_id: pickedAgentId.value,
        title: text.slice(0, 30)
      })
      sid = r.data.id
      store.setCurrentSession(r.data)
      // 立即插入侧边栏会话列表（不等 AI 回复完）
      if (!store.sessions.find(s => s.id === r.data.id)) {
        store.sessions.unshift(r.data)
      }
      // 静默更新 URL，不触发 watcher 避免中断流式输出
      window.history.replaceState(null, '', `/chat/${pickedAgentId.value}/${sid}`)
    } catch { return ElMessage.error('创建会话失败') }
  }

  msgs.value.push({ role: 'user', content: text })
  await scrollBottom()

  // SSE 流式
  streaming.value = true
  streamText.value = ''

// ... existing code ...
  try {
    const resp = await chatStream(sid, 1, text)

    // 检查 HTTP 状态
    if (!resp.ok) {
      const errText = await resp.text()
      try {
        const errJson = JSON.parse(errText)
        throw new Error(errJson.detail || errText)
      } catch (e) {
        if (e.message !== errText) throw e
        throw new Error(errText || `HTTP ${resp.status}`)
      }
    }

    const reader = resp.body.getReader()
    const dec = new TextDecoder()
    let buf = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buf += dec.decode(value, { stream: true })
      const lines = buf.split('\n')
      buf = lines.pop() || ''

      for (const line of lines) {
        if (!line.trim()) continue

        // 尝试解析 SSE 格式
        if (line.startsWith('data: ')) {
          const raw = line.slice(6)
          try {
            const json = JSON.parse(raw)
            if (json.error) {
              streamText.value = '[错误] ' + json.error
            } else if (json.content) {
              streamText.value += json.content
            }
          } catch {
            // 如果解析失败，直接拼接原始内容
            streamText.value += raw
          }
        } else {
          // 非 data: 开头的行，直接拼接（兼容后端未使用 SSE 格式）
          streamText.value += line
        }
      }

      // 实时滚动到底部
      await scrollBottom()
    }
   } catch (e) {
    streamText.value = '[请求失败] ' + (e.message || '未知错误')
  }

  // 流式结束后保存 AI 消息
  const finalText = streamText.value.trim()

  // 只要有有效内容就添加到消息列表
  if (finalText && !finalText.startsWith('[请求失败]') && !finalText.startsWith('[错误]')) {
    msgs.value.push({ role: 'assistant', content: streamText.value })
  } else if (streamText.value && !streamText.value.startsWith('[请求失败]')) {
    // 即使 trim 后为空，只要不是错误信息也添加（可能是纯换行等）
    msgs.value.push({ role: 'assistant', content: streamText.value })
  }

  streamText.value = ''
  streaming.value = false
  await scrollBottom()
}

// ... existing code ...


async function scrollBottom() {
  await nextTick()
  if (msgArea.value) msgArea.value.scrollTop = msgArea.value.scrollHeight
}

// 路由变化：有会话→加载历史，无会话→清空
watch(() => route.path, async (path) => {
  const { agentId, sessionId } = route.params
  if (agentId && sessionId) {
    pickedAgentId.value = Number(agentId)
    const agent = store.agents.find(a => a.id === pickedAgentId.value)
    if (agent) store.setCurrentAgent(agent)
    store.setCurrentSession({ id: Number(sessionId), agent_id: Number(agentId) })
    await loadHistory(Number(sessionId))
  } else if (path === '/chat') {
    // 新对话：清空
    msgs.value = []
    pickedAgentId.value = null
    store.clearChat()
  }
})
</script>

<style scoped>
.chat-view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 顶部 */
.chat-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-primary);
}
.agent-pick { width: 280px; }
.agent-tag {
  font-size: 13px;
  color: var(--accent);
  background: var(--accent-light);
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 500;
}

/* 消息区 */
.msg-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* 欢迎 */
.welcome {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  gap: 8px;
}
.welcome-icon { color: #d0d0d8; margin-bottom: 8px; }
.welcome h2 { font-weight: 600; font-size: 20px; color: var(--text-secondary); }
.welcome p  { font-size: 14px; }

/* 流式临时气泡 */
.msg-row {
  display: flex;
  gap: 12px;
  max-width: 85%;
  margin-bottom: 12px;
}
.msg-row.assistant { align-self: flex-start; }
.msg-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: var(--bg-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 4px;
}
.msg-bubble {
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}
.msg-bubble.streaming { background: var(--bg-primary); }
.cursor { animation: blink 1s infinite; color: var(--accent); }
@keyframes blink { 0%,50% { opacity:1; } 51%,100% { opacity:0; } }
</style>
