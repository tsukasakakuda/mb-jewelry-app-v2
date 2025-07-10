<template>
  <div class="sidebar-container">
    <!-- Mobile Menu Toggle -->
    <button 
      @click="toggleMenu" 
      class="mobile-menu-btn md:hidden fixed top-4 left-4 z-50 p-3 bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl text-white hover:bg-white/20 transition-all duration-200"
    >
      <svg 
        class="w-6 h-6 transform transition-transform duration-200" 
        :class="{ 'rotate-90': isOpen }"
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          v-if="!isOpen"
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"
        />
        <path 
          v-else
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2"
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>

    <!-- Mobile Menu Overlay -->
    <div 
      v-if="isOpen" 
      class="mobile-overlay md:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
      @click="closeMenu"
    ></div>

    <!-- Mobile Sidebar -->
    <div 
      :class="[
        'mobile-sidebar md:hidden fixed top-0 left-0 h-full w-80 bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 transform transition-transform duration-300 ease-in-out z-40',
        isOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="flex flex-col h-full backdrop-blur-xl bg-white/5 border-r border-white/10">
        <!-- Mobile Header -->
        <div class="p-6 border-b border-white/10">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm3.5 6L12 10.5 8.5 8 12 5.5 15.5 8zM12 21.5c-5.24 0-9.5-4.26-9.5-9.5S6.76 2.5 12 2.5s9.5 4.26 9.5 9.5-4.26 9.5-9.5 9.5z"/>
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-white">MB Jewelry</h2>
              <p class="text-white/60 text-xs">ツールメニュー</p>
            </div>
          </div>
        </div>

        <!-- Mobile Navigation -->
        <nav class="flex-1 p-6">
          <ul class="space-y-3">
            <li>
              <router-link 
                to="/" 
                @click="closeMenu"
                class="nav-link group flex items-center space-x-3 p-3 rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200"
                :class="{ 'bg-white/10 text-white': $route.path === '/' }"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                </svg>
                <span class="font-medium">メインメニュー</span>
              </router-link>
            </li>
            <li>
              <router-link 
                to="/calculate" 
                @click="closeMenu"
                class="nav-link group flex items-center space-x-3 p-3 rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200"
                :class="{ 'bg-white/10 text-white': $route.path === '/calculate' }"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
                </svg>
                <span class="font-medium">地金計算</span>
              </router-link>
            </li>
            <li>
              <router-link 
                to="/csv" 
                @click="closeMenu"
                class="nav-link group flex items-center space-x-3 p-3 rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200"
                :class="{ 'bg-white/10 text-white': $route.path === '/csv' }"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                  <path d="M14 2v6h6"/>
                  <path d="M16 13H8"/>
                  <path d="M16 17H8"/>
                  <path d="M10 9H8"/>
                </svg>
                <span class="font-medium">CSV加工</span>
              </router-link>
            </li>
          </ul>
        </nav>

        <!-- Mobile Logout -->
        <div class="p-6 border-t border-white/10">
          <button 
            @click="handleLogout" 
            class="logout-btn w-full flex items-center justify-center space-x-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 hover:text-white p-3 rounded-xl transition-all duration-200 border border-red-500/30 hover:border-red-500/50"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/>
            </svg>
            <span class="font-medium">ログアウト</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Desktop Sidebar -->
    <div class="desktop-sidebar hidden md:flex fixed top-0 left-0 h-full w-64 bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 flex-col z-30">
      <div class="flex flex-col h-full backdrop-blur-xl bg-white/5 border-r border-white/10">
        <!-- Desktop Header -->
        <div class="p-6 border-b border-white/10">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm3.5 6L12 10.5 8.5 8 12 5.5 15.5 8zM12 21.5c-5.24 0-9.5-4.26-9.5-9.5S6.76 2.5 12 2.5s9.5 4.26 9.5 9.5-4.26 9.5-9.5 9.5z"/>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold text-white tracking-wide">MB Jewelry</h2>
              <p class="text-white/60 text-sm">ツールメニュー</p>
            </div>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <nav class="flex-1 p-6">
          <ul class="space-y-4">
            <li>
              <router-link 
                to="/" 
                class="nav-link group flex items-center space-x-4 p-4 rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200 border border-transparent hover:border-white/20"
                :class="{ 'bg-white/10 text-white border-white/20': $route.path === '/' }"
              >
                <div class="flex items-center justify-center w-10 h-10 bg-white/10 rounded-lg group-hover:bg-white/20 transition-colors">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                  </svg>
                </div>
                <div>
                  <span class="font-medium">メインメニュー</span>
                  <p class="text-white/50 text-xs mt-1">ダッシュボード</p>
                </div>
              </router-link>
            </li>
            <li>
              <router-link 
                to="/calculate" 
                class="nav-link group flex items-center space-x-4 p-4 rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200 border border-transparent hover:border-white/20"
                :class="{ 'bg-white/10 text-white border-white/20': $route.path === '/calculate' }"
              >
                <div class="flex items-center justify-center w-10 h-10 bg-blue-500/20 rounded-lg group-hover:bg-blue-500/30 transition-colors">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
                  </svg>
                </div>
                <div>
                  <span class="font-medium">地金計算</span>
                  <p class="text-white/50 text-xs mt-1">価格計算ツール</p>
                </div>
              </router-link>
            </li>
            <li>
              <router-link 
                to="/csv" 
                class="nav-link group flex items-center space-x-4 p-4 rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200 border border-transparent hover:border-white/20"
                :class="{ 'bg-white/10 text-white border-white/20': $route.path === '/csv' }"
              >
                <div class="flex items-center justify-center w-10 h-10 bg-green-500/20 rounded-lg group-hover:bg-green-500/30 transition-colors">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                    <path d="M14 2v6h6"/>
                    <path d="M16 13H8"/>
                    <path d="M16 17H8"/>
                    <path d="M10 9H8"/>
                  </svg>
                </div>
                <div>
                  <span class="font-medium">CSV加工</span>
                  <p class="text-white/50 text-xs mt-1">データ処理ツール</p>
                </div>
              </router-link>
            </li>
          </ul>
        </nav>

        <!-- Desktop Logout -->
        <div class="p-6 border-t border-white/10">
          <button 
            @click="handleLogout" 
            class="logout-btn w-full flex items-center justify-center space-x-3 bg-red-500/20 hover:bg-red-500/30 text-red-200 hover:text-white p-4 rounded-xl transition-all duration-200 border border-red-500/30 hover:border-red-500/50 group"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/>
            </svg>
            <span class="font-medium">ログアウト</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { removeToken } from '@/utils/auth.js'

export default {
  name: 'SidebarMenu',
  setup() {
    const router = useRouter()
    
    const handleLogout = () => {
      removeToken()
      router.push('/login')
    }
    
    return {
      handleLogout
    }
  },
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen
    },
    closeMenu() {
      this.isOpen = false
    }
  },
  mounted() {
    this.$router.afterEach(() => {
      this.isOpen = false
    })
  }
}
</script>

<style scoped>
.sidebar-container {
  position: relative;
}

.mobile-menu-btn {
  transform: translateZ(0);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.mobile-menu-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.mobile-sidebar {
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.3);
}

.desktop-sidebar {
  box-shadow: 5px 0 20px rgba(0, 0, 0, 0.1);
}

.nav-link {
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.nav-link:hover::before {
  left: 100%;
}

.logout-btn {
  position: relative;
  overflow: hidden;
}

.logout-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(220, 38, 38, 0.2);
}

.logout-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.logout-btn:hover::before {
  left: 100%;
}

.router-link-active {
  color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

@media (max-width: 768px) {
  .mobile-sidebar {
    backdrop-filter: blur(20px);
  }
}

.mobile-sidebar .nav-link {
  animation: slideInLeft 0.3s ease-out forwards;
}

.mobile-sidebar .nav-link:nth-child(1) {
  animation-delay: 0.1s;
}

.mobile-sidebar .nav-link:nth-child(2) {
  animation-delay: 0.2s;
}

.mobile-sidebar .nav-link:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>