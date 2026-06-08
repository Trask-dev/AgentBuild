<template>
  <div class="session-list" ref="listRef">
    <div v-if="sessions.length === 0" class="empty">暂无会话记录</div>
    <div
      v-for="s in sessions"
      :key="s.id"
      class="session-item"
      :class="{ active: store.currentSession?.id === s.id }"
      @click="select(s)"
    >
      <el-icon :size="15"><ChatDotRound /></el-icon>
      <span class="title">{{ s.title || '新对话' }}</span>
      <button class="del-btn" @click.stop="remove(s)">
        <el-icon :size="13"><Close /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { getSessions, deleteSession } from '../api/session'

const props = defineProps({ filterAgentId: { type: Number, default: null } })
const router = useRouter()
const store = useAppStore()
const sessions = ref([])

async function load() {
  try {
    const r = await getSessions(props.filterAgentId || undefined)
    sessions.value = r.data
    store.setSessions(r.data)
  } catch { sessions.value = [] }
}

onMounted(load)
watch(() => props.filterAgentId, load)

function select(s) {
  store.setCurrentSession(s)
  const agent = store.agents.find(a => a.id === s.agent_id)
  if (agent) store.setCurrentAgent(agent)
  store.setMenuActive('chat')
  router.push(`/chat/${s.agent_id}/${s.id}`)
}

async function remove(s) {
  try {
    await deleteSession(s.id)
    if (store.currentSession?.id === s.id) store.clearChat()
    load()
  } catch {}
}

defineExpose({ load })
</script>

<style scoped>
.session-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.empty {
  text-align: center;
  color: var(--text-tertiary);
  font-size: 13px;
  padding: 24px 0;
}
.session-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 14px;
  transition: all .15s;
  position: relative;
}
.session-item:hover { background: var(--bg-hover); }
.session-item.active { background: var(--bg-active); color: var(--text-primary); font-weight: 500; }
.title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.del-btn {
  opacity: 0;
  border: none;
  background: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
}
.session-item:hover .del-btn { opacity: 1; }
.del-btn:hover { color: #e74c3c; background: rgba(231,76,60,.1); }
</style>
