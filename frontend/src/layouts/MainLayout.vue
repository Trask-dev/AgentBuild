<template>
  <div class="main-layout">
    <TheSidebar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import TheSidebar from '../components/TheSidebar.vue'
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}
.main-content {
  flex: 1;
  background: var(--bg-primary);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
