<script setup>
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Uploader from './components/Uploader.vue'
import DocumentList from './components/DocumentList.vue'
import DocumentModal from './components/DocumentModal.vue'

const dashboardKey = ref(0)
const documentListRef = ref(null)
const selectedDocument = ref(null)

function refreshDashboard() {
  // Force Dashboard to re-fetch stats after a new upload
  dashboardKey.value++
  // Also refresh the document list
  if (documentListRef.value) {
    documentListRef.value.fetchDocuments()
  }
}

function handleSelectDocument(doc) {
  selectedDocument.value = doc
}

function handleCloseModal() {
  selectedDocument.value = null
}
</script>

<template>
  <div class="container-fluid px-3 px-md-4 px-lg-5 py-3 py-md-4">
    <header class="mb-3 mb-md-4">
      <h1 class="display-6 display-md-5 fw-bold text-primary">Lekhan-AI</h1>
      <p class="text-muted small small-md">Administrative Document Assistant</p>
    </header>

    <main>
      <Dashboard :key="dashboardKey" />

      <div class="mt-3 mt-md-4">
        <Uploader @uploaded="refreshDashboard" />
      </div>

      <div class="mt-3 mt-md-4">
        <DocumentList ref="documentListRef" @select="handleSelectDocument" />
      </div>

      <!-- Hidden Modal Component -->
      <DocumentModal 
        :document="selectedDocument" 
        @close="handleCloseModal" 
      />
    </main>
  </div>
</template>

<style scoped></style>
