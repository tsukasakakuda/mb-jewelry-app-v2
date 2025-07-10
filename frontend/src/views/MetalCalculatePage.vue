<template>
  <div class="min-h-screen relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div class="absolute inset-0 pattern-bg"></div>
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full opacity-20 blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full opacity-15 blur-3xl animate-pulse delay-1000"></div>
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
  opacity: 0.3;
  background-image: radial-gradient(circle at 30px 30px, rgba(255, 255, 255, 0.05) 2px, transparent 2px);
  background-size: 60px 60px;
}
</style>