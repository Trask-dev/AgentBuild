import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const agents = ref([])
  const sessions = ref([])
  const currentAgent = ref(null)
  const currentSession = ref(null)
  const menuActive = ref('chat')

  const currentAgentId = computed(() => currentAgent.value?.id ?? null)
  const currentSessionId = computed(() => currentSession.value?.id ?? null)

  function setAgents(list) { agents.value = list }
  function setSessions(list) { sessions.value = list }
  function setCurrentAgent(agent) { currentAgent.value = agent }
  function setCurrentSession(session) { currentSession.value = session }
  function setMenuActive(v) { menuActive.value = v }

  function clearChat() {
    currentAgent.value = null
    currentSession.value = null
  }

  return {
    agents, sessions, currentAgent, currentSession, menuActive,
    currentAgentId, currentSessionId,
    setAgents, setSessions, setCurrentAgent, setCurrentSession,
    setMenuActive, clearChat
  }
})
