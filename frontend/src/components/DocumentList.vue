<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const documents = ref([])

async function fetchDocuments() {
  try {
    const response = await axios.get(`${API_URL}/documents`)
    documents.value = response.data
  } catch (error) {
    console.error('Failed to fetch documents:', error)
  }
}

function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function getCategoryBadgeClass(category) {
  switch (category) {
    case 'Circular':
      return 'bg-success'
    case 'Memo':
      return 'bg-warning text-dark'
    case 'Notification':
      return 'bg-info text-dark'
    default:
      return 'bg-secondary'
  }
}

onMounted(() => {
  fetchDocuments()
})

defineExpose({ fetchDocuments })
</script>

<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body">
      <h5 class="card-title mb-3">Processed Documents</h5>

      <div v-if="documents.length === 0" class="text-center text-muted py-4">
        <p>No documents have been processed yet.</p>
        <p class="small">Upload a document to get started.</p>
      </div>

      <div v-else class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Filename</th>
              <th scope="col">Category</th>
              <th scope="col">Upload Date</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="doc in documents"
              :key="doc.id"
              style="cursor: pointer;"
              @click="$emit('select', doc)"
            >
              <td>{{ doc.id }}</td>
              <td class="fw-medium">{{ doc.filename }}</td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="getCategoryBadgeClass(doc.category)"
                >
                  {{ doc.category || 'Processing...' }}
                </span>
              </td>
              <td class="text-muted small">{{ formatDate(doc.upload_date) }}</td>
              <td>
                <span v-if="doc.summary" class="text-success">✓ Ready</span>
                <span v-else class="text-warning">⏳ Processing</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
