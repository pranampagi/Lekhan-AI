<script setup>
import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const emit = defineEmits(['uploaded'])

const isDragging = ref(false)
const isUploading = ref(false)
const uploadMessage = ref('')
const uploadError = ref('')

function handleDragOver(event) {
  event.preventDefault()
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function handleDrop(event) {
  event.preventDefault()
  isDragging.value = false

  const files = event.dataTransfer.files
  if (files.length > 0) {
    uploadFile(files[0])
  }
}

function handleFileSelect(event) {
  const files = event.target.files
  if (files.length > 0) {
    uploadFile(files[0])
  }
}

async function uploadFile(file) {
  // Validate file type on the client side
  const allowedTypes = ['application/pdf', 'text/plain']
  if (!allowedTypes.includes(file.type)) {
    uploadError.value = 'Only PDF and text files are accepted.'
    uploadMessage.value = ''
    return
  }

  isUploading.value = true
  uploadError.value = ''
  uploadMessage.value = ''

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    uploadMessage.value = `"${response.data.filename}" uploaded successfully! Processing in background...`
    emit('uploaded')
  } catch (error) {
      uploadError.value = error.response?.data?.detail || 'Upload failed. Please try again.'
  } finally {
      isUploading.value = false
  }
}
</script>

<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body p-4">
      <h5 class="card-title mb-3">Upload Document</h5>

      <!-- Drag and Drop Zone -->
      <div
        class="upload-zone rounded-3 text-center p-5"
        :class="{ 'drag-active': isDragging }"
        @dragover="handleDragOver"
        @dragleave="handleDragLeave"
        @drop="handleDrop"
      >
        <div v-if="isUploading">
          <div class="spinner-border text-primary mb-3" role="status">
            <span class="visually-hidden">Uploading...</span>
          </div>
          <p class="text-muted">Uploading file...</p>
        </div>

        <div v-else>
          <div class="fs-1 mb-2">📄</div>
          <p class="text-muted mb-2">Drag & drop your document here</p>
          <p class="text-muted small mb-3">or</p>
          <label class="btn btn-primary btn-sm">
            Browse Files
            <input
              type="file"
              class="d-none"
              accept=".pdf,.txt"
              @change="handleFileSelect"
            />
          </label>
          <p class="text-muted small mt-2 mb-0">Supports PDF and TXT files</p>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="uploadMessage" class="alert alert-success mt-3 mb-0" role="alert">
        {{ uploadMessage }}
      </div>

      <!-- Error Message -->
      <div v-if="uploadError" class="alert alert-danger mt-3 mb-0" role="alert">
        {{ uploadError }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-zone {
  border: 2px dashed #dee2e6;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-zone:hover,
.upload-zone.drag-active {
  border-color: #0d6efd;
  background-color: #e7f1ff;
}
</style>
