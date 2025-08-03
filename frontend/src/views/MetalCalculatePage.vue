<template>
  <div class="min-h-screen relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200">
      <div class="absolute inset-0 pattern-bg"></div>
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full opacity-10 blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-red-400 to-red-500 rounded-full opacity-8 blur-3xl animate-pulse delay-1000"></div>
    </div>
    
    <div class="relative z-10">
      <MetalCalculate />
    </div>
  </div>
</template>
  
<script>
import MetalCalculate from '@/components/MetalCalculate.vue';

export default {
  components: { MetalCalculate },
};
</script>

<style scoped>
.pattern-bg {
  opacity: 0.2;
  background-image: radial-gradient(circle at 20px 20px, rgba(255, 255, 255, 0.1) 2px, transparent 2px);
  background-size: 40px 40px;
}
</style>