import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/agent': {
        target: 'http://localhost:8000',
        bypass(req) {
          // 浏览器刷新 SPA 页面（如 /agents）时返回 index.html，不转发给后端
          if (req.headers.accept?.includes('text/html')) return '/index.html'
        }
      },
      '/chat': {
        target: 'http://localhost:8000',
        bypass(req) {
          if (req.headers.accept?.includes('text/html')) return '/index.html'
        }
      },
      '/rag':    'http://localhost:8000',
      '/session':'http://localhost:8000'
    }
  }
})
