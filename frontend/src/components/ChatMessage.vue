<template>
  <div class="msg-row" :class="role">
    <div class="msg-avatar">
      <el-icon v-if="role === 'user'" :size="16"><User /></el-icon>
      <el-icon v-else :size="16"><Cpu /></el-icon>
    </div>
    <div class="msg-bubble">
      {{ content }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  role:    { type: String, required: true },
  content: { type: String, required: true }
})
</script>

<style scoped>
.msg-row {
  display: flex;
  gap: 12px;
  max-width: 85%;
  margin-bottom: 4px;
}
.msg-row.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}
.msg-row.assistant {
  align-self: flex-start;
}

.msg-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.msg-row.user .msg-avatar      { background: #eef2ff; color: var(--accent); }
.msg-row.assistant .msg-avatar { background: #f0fdf4; color: #22c55e; }

.msg-bubble {
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}
.msg-row.user .msg-bubble {
  background: #eef2ff;
  color: var(--text-primary);
  border-bottom-right-radius: 4px;
}
.msg-row.assistant .msg-bubble {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}
</style>
