import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/chat',
    children: [
      {
        path: 'chat',
        name: 'Chat',
        component: () => import('../views/ChatView.vue')
      },
      {
        path: 'chat/:agentId/:sessionId',
        name: 'ChatSession',
        component: () => import('../views/ChatView.vue')
      },
      {
        path: 'agents',
        name: 'Agents',
        component: () => import('../views/AgentView.vue')
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('../views/KnowledgeView.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
