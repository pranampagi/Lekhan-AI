<script setup>
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Uploader from './components/Uploader.vue'

const dashboardKey = ref(0)

function refreshDashboard() {
  // Force Dashboard to re-fetch stats after a new upload
  dashboardKey.value++
}
</script>

<template>
  <div class="container py-4">
    <header class="mb-4">
      <h1 class="display-5 fw-bold text-primary">Lekhan-AI</h1>
      <p class="text-muted">Administrative Document Assistant</p>
    </header>

    <main>
      <Dashboard :key="dashboardKey" />

      <div class="mt-4">
        <Uploader @uploaded="refreshDashboard" />
      </div>
    </main>
  </div>
</template>

<style scoped></style>
