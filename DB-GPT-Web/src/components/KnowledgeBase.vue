<template>
  <div>
    <!-- ... existing code ... -->
    <div v-for="item in knowledgeBaseItems" :key="item.id" v-tooltip="{ content: item.description }">
      <!-- ... existing code ... -->
    </div>
    <!-- ... existing code ... -->
  </div>
</template>

<script>
// ... existing code ...
</script>