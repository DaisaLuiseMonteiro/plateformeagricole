<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<style>
/* Masquer les scrollbars globalement */
::-webkit-scrollbar {
  display: none;
}

html, body {
  margin: 0;
  padding: 0;
  -ms-overflow-style: none;
  scrollbar-width: none;
  overflow: -moz-scrollbars-none;
}
</style>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
