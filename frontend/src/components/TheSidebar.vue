<template>
  <aside class="sidebar">
    <!-- Logo -->
    <div class="logo" @click="goChat">
      <div class="logo-icon"><el-icon :size="22"><Cpu /></el-icon></div>
      <span class="logo-text">AgentHub</span>
    </div>

    <!-- 新对话按钮 -->
    <div class="nav-actions">
      <button class="btn-new-chat" @click="goChat">
        <el-icon :size="18"><Plus /></el-icon>
        <span>新对话</span>
      </button>

      <nav class="nav-menu">
        <button
          class="nav-item"
          :class="{ active: store.menuActive === 'agents' }"
          @click="goAgents"
        >
          <el-icon :size="18"><UserFilled /></el-icon>
          <span>智能体</span>
        </button>
        <button
          class="nav-item"
          :class="{ active: store.menuActive === 'knowledge' }"
          @click="goKnowledge"
        >
          <el-icon :size="18"><FolderOpened /></el-icon>
          <span>知识库</span>
        </button>
      </nav>
    </div>

    <!-- 分隔 -->
    <div class="divider"></div>

    <!-- 会话历史 -->
    <div class="session-area">
      <div class="session-header">
        <span>会话历史</span>
        <el-select
          v-model="filterAgentId"
          placeholder="全部"
          size="small"
          clearable
          class="filter-select"
        >
          <el-option v-for="a in store.agents" :key="a.id" :label="a.name" :value="a.id" />
        </el-select>
      </div>
      <SessionList :filter-agent-id="filterAgentId" />
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { getAgents } from '../api/agent'
import SessionList from './SessionList.vue'

const router = useRouter()
const store = useAppStore()
const filterAgentId = ref(null)

onMounted(async () => {
  try { const r = await getAgents(); store.setAgents(r.data) } catch {}
})

function goChat() {
  store.clearChat()
  store.setMenuActive('chat')
  router.push('/chat')
}
function goAgents() {
  store.setMenuActive('agents')
  router.push('/agents')
}
function goKnowledge() {
  store.setMenuActive('knowledge')
  router.push('/knowledge')
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100vh;
  background: var(--bg-secondary);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border);
  user-select: none;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 20px 16px;
  cursor: pointer;
}
.logo-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

/* 导航 */
.nav-actions { padding: 0 16px; }
.btn-new-chat {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 0;
  border: none;
  border-radius: var(--radius);
  background: var(--accent);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background .2s;
  margin-bottom: 12px;
}
.btn-new-chat:hover { background: var(--accent-hover); }

.nav-menu { display: flex; flex-direction: column; gap: 2px; }
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: none;
  border-radius: var(--radius);
  background: transparent;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all .15s;
  text-align: left;
}
.nav-item:hover { background: var(--bg-hover); color: var(--text-primary); }
.nav-item.active { background: var(--bg-active); color: var(--text-primary); font-weight: 500; }

/* 分隔线 */
.divider {
  height: 1px;
  background: var(--border);
  margin: 14px 16px;
}

/* 会话区 */
.session-area {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 0 12px 12px;
}
.session-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px 8px;
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
}
.filter-select { width: 110px; }
</style>
