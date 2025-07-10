<template>
  <div class="app-container">
    <SidebarMenu />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import SidebarMenu from './components/SidebarMenu.vue';
export default { components: { SidebarMenu } };
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
  margin: 0;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
  color: #ffffff;
}

.app-container {
  min-height: 100vh;
  display: flex;
  position: relative;
}

.main-content {
  flex: 1;
  margin-left: 0;
  transition: margin-left 0.3s ease;
}

@media (min-width: 768px) {
  .main-content {
    margin-left: 256px;
  }
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Selection styling */
::selection {
  background: rgba(255, 193, 7, 0.3);
  color: white;
}

/* Focus ring styling */
:focus-visible {
  outline: 2px solid rgba(255, 193, 7, 0.6);
  outline-offset: 2px;
}

/* Animation for route transitions */
.router-enter-active,
.router-leave-active {
  transition: opacity 0.3s ease;
}

.router-enter-from,
.router-leave-to {
  opacity: 0;
}
</style>