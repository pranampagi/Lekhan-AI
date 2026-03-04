<script setup>
const props = defineProps({
  document: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close'])

function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString + 'Z')
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function handleClose() {
  emit('close')
}
</script>

<template>
  <!-- Backdrop -->
  <div v-if="document" class="modal-backdrop fade show" @click="handleClose"></div>

  <!-- Modal -->
  <div
    v-if="document"
    class="modal fade show d-block"
    tabindex="-1"
    role="dialog"
    @click.self="handleClose"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-light">
          <h5 class="modal-title">
            <span class="text-primary">Summary:</span> {{ document.filename }}
          </h5>
          <button
            type="button"
            class="btn-close"
            aria-label="Close"
            @click="handleClose"
          ></button>
        </div>

        <div class="modal-body p-4">
          <div class="mb-4">
            <h6 class="text-muted text-uppercase small fw-bold mb-2">AI Generated Summary</h6>
            <div class="p-3 bg-light rounded-3 border">
              <p v-if="document.summary" class="mb-0 leading-relaxed">
                {{ document.summary }}
              </p>
              <div v-else class="text-center py-3">
                <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                <span class="text-muted">Processing summary...</span>
              </div>
            </div>
          </div>

          <div class="row g-3">
            <div class="col-sm-6">
              <h6 class="text-muted text-uppercase small fw-bold mb-1">Classification</h6>
              <span
                class="badge rounded-pill px-3"
                :class="{
                  'bg-success': document.category === 'Circular',
                  'bg-warning text-dark': document.category === 'Memo',
                  'bg-info text-dark': document.category === 'Notification',
                  'bg-secondary': !document.category
                }"
              >
                {{ document.category || 'Categorizing...' }}
              </span>
            </div>
            <div class="col-sm-6">
              <h6 class="text-muted text-uppercase small fw-bold mb-1">Uploaded On</h6>
              <p class="text-dark small mb-0">{{ formatDate(document.upload_date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.leading-relaxed {
  line-height: 1.6;
}
</style>
