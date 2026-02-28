<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const stats = ref({
  totalDocuments: 0,
  circulars: 0,
  memos: 0,
  notifications: 0,
})

async function fetchStats() {
  try {
    const response = await axios.get(`${API_URL}/documents`)
    const documents = response.data

    stats.value.totalDocuments = documents.length
    stats.value.circulars = documents.filter(d => d.category === 'Circular').length
    stats.value.memos = documents.filter(d => d.category === 'Memo').length
    stats.value.notifications = documents.filter(d => d.category === 'Notification').length
  } catch (error) {
    console.error('Failed to fetch document stats:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<template>
  <div class="row g-4">
    <!-- Total Documents Card -->
    <div class="col-md-6 col-lg-3">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body text-center">
          <div class="fs-1 fw-bold text-primary">{{ stats.totalDocuments }}</div>
          <div class="text-muted mt-2">Total Processed</div>
        </div>
      </div>
    </div>

    <!-- Circulars Card -->
    <div class="col-md-6 col-lg-3">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body text-center">
          <div class="fs-1 fw-bold text-success">{{ stats.circulars }}</div>
          <div class="text-muted mt-2">Circulars</div>
        </div>
      </div>
    </div>

    <!-- Memos Card -->
    <div class="col-md-6 col-lg-3">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body text-center">
          <div class="fs-1 fw-bold text-warning">{{ stats.memos }}</div>
          <div class="text-muted mt-2">Memos</div>
        </div>
      </div>
    </div>

    <!-- Notifications Card -->
    <div class="col-md-6 col-lg-3">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body text-center">
          <div class="fs-1 fw-bold text-info">{{ stats.notifications }}</div>
          <div class="text-muted mt-2">Notifications</div>
        </div>
      </div>
    </div>
  </div>
</template>
