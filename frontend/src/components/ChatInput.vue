<template>
  <div class="input-area">
    <div class="input-box">
      <textarea
        ref="ta"
        v-model="text"
        class="input-ta"
        :placeholder="placeholder"
        :disabled="disabled"
        :rows="1"
        @input="autoGrow"
        @keydown="onKey"
      ></textarea>
      <button
        class="send-btn"
        :class="{ active: text.trim() && !disabled }"
        :disabled="!text.trim() || disabled"
        @click="send"
      >
        <el-icon :size="20"><Promotion /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
  placeholder: { type: String, default: '输入消息，Enter 发送，Shift+Enter 换行' }
})
const emit = defineEmits(['send'])
const text = ref('')
const ta = ref(null)

function autoGrow() {
  const el = ta.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 200) + 'px'
}

function onKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

function send() {
  const v = text.value.trim()
  if (!v) return
  emit('send', v)
  text.value = ''
  nextTick(() => {
    if (ta.value) ta.value.style.height = 'auto'
  })
}
</script>

<style scoped>
.input-area {
  padding: 0 24px 20px;
  background: var(--bg-primary);
}
.input-box {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 8px 8px 8px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid transparent;
  transition: border .2s, box-shadow .2s;
}
.input-box:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(79,70,229,.1);
}
.input-ta {
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  background: transparent;
  font-size: 15px;
  line-height: 1.5;
  padding: 4px 0;
  color: var(--text-primary);
  font-family: inherit;
  max-height: 200px;
}
.input-ta::placeholder { color: var(--text-tertiary); }
.input-ta:disabled { opacity: .5; }

.send-btn {
  width: 36px; height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--bg-hover);
  color: var(--text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all .2s;
}
.send-btn.active {
  background: var(--accent);
  color: #fff;
}
.send-btn.active:hover { background: var(--accent-hover); }
</style>
