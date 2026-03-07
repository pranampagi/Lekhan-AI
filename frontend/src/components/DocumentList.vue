<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const documents = ref([])
const isLoading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')

const categories = ['Circular', 'Memo', 'Notification']

const filteredDocuments = computed(() => {
  return documents.value.filter((doc) => {
    const matchesSearch =
      !searchQuery.value ||
      doc.filename.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesCategory =
      !selectedCategory.value || doc.category === selectedCategory.value

    return matchesSearch && matchesCategory
  })
})

async function fetchDocuments() {
  isLoading.value = true
  try {
    const response = await axios.get(`${API_URL}/documents`)
    documents.value = response.data
  } catch (error) {
    console.error('Failed to fetch documents:', error)
  } finally {
    isLoading.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return '—'
  // Append 'Z' to ensure the naive timestamp from the backend is treated as UTC
  // so the browser correctly converts it to the user's local timezone (IST).
  const date = new Date(dateString + 'Z')
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

function clearFilters() {
  searchQuery.value = ''
  selectedCategory.value = ''
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

      <!-- Loading Spinner -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading documents...</span>
        </div>
        <p class="text-muted mt-2">Loading documents...</p>
      </div>

      <!-- Search and Filter Controls -->
      <div class="row g-2 mb-3">
        <div class="col-md-6">
          <input
            v-model="searchQuery"
            type="text"
            class="form-control"
            placeholder="Search by filename..."
          />
        </div>
        <div class="col-md-4">
          <select v-model="selectedCategory" class="form-select">
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
        </div>
        <div class="col-md-2">
          <button
            class="btn btn-outline-secondary w-100"
            @click="clearFilters"
            :disabled="!searchQuery && !selectedCategory"
          >
            Clear
          </button>
        </div>
      </div>

      <div v-if="filteredDocuments.length === 0" class="text-center text-muted py-4">
        <p v-if="documents.length === 0">No documents have been processed yet.</p>
        <p v-else>No documents match your search criteria.</p>
        <p class="small">
          <span v-if="documents.length === 0">Upload a document to get started.</span>
          <span v-else>
            <a href="#" class="text-decoration-none" @click.prevent="clearFilters">Clear filters</a>
            to see all documents.
          </span>
        </p>
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
              v-for="doc in filteredDocuments"
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

        <p class="text-muted small mb-0">
          Showing {{ filteredDocuments.length }} of {{ documents.length }} document(s)
        </p>
      </div>
    </div>
  </div>
</template>
