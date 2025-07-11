<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 relative overflow-hidden">
    <!-- Background Animation -->
    <div class="absolute inset-0">
      <div class="absolute top-0 left-0 w-full h-full pattern-bg"></div>
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-blue-400/10 to-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 left-1/4 w-80 h-80 bg-gradient-to-r from-green-400/10 to-green-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Header -->
    <header class="relative z-10 px-6 py-8">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm3.5 6L12 10.5 8.5 8 12 5.5 15.5 8zM12 21.5c-5.24 0-9.5-4.26-9.5-9.5S6.76 2.5 12 2.5s9.5 4.26 9.5 9.5-4.26 9.5-9.5 9.5z"/>
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-800 tracking-wide">MB Jewelry</h1>
            <p class="text-gray-600 text-sm">プロフェッショナルツールスイート</p>
          </div>
        </div>
        <button 
          @click="handleLogout"
          class="logout-btn group flex items-center space-x-2 bg-red-50 hover:bg-red-100 text-red-600 hover:text-red-700 px-4 py-2 rounded-xl transition-all duration-200 backdrop-blur-sm border border-red-200 hover:border-red-300"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/>
          </svg>
          <span>ログアウト</span>
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 max-w-7xl mx-auto px-6 pb-12">
      <!-- Welcome Section -->
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-gray-800 mb-4 tracking-wide">メインメニュー</h2>
        <p class="text-gray-600 text-lg max-w-2xl mx-auto">高精度な地金計算とデータ加工ツールで、ジュエリービジネスを効率化しましょう。</p>
      </div>

      <!-- Menu Cards -->
      <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <!-- Metal Calculator Card -->
        <div class="menu-card group">
          <router-link to="/calculate" class="block">
            <div class="card-inner backdrop-blur-sm bg-white/80 border border-gray-200 rounded-2xl p-8 hover:bg-white/90 transition-all duration-300 hover:shadow-2xl hover:border-gray-300">
              <div class="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-400 to-cyan-500 rounded-xl mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-800 mb-3">地金自動計算</h3>
              <p class="text-gray-600 mb-4">ゴールド、シルバー、プラチナの価格をリアルタイムで精密計算</p>
              <div class="flex items-center text-blue-600 group-hover:text-blue-700 transition-colors">
                <span class="mr-2">計算を開始</span>
                <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </div>
            </div>
          </router-link>
        </div>

        <!-- CSV Processing Card -->
        <div class="menu-card group">
          <router-link to="/csv" class="block">
            <div class="card-inner backdrop-blur-sm bg-white/80 border border-gray-200 rounded-2xl p-8 hover:bg-white/90 transition-all duration-300 hover:shadow-2xl hover:border-gray-300">
              <div class="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-xl mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                  <path d="M14 2v6h6"/>
                  <path d="M16 13H8"/>
                  <path d="M16 17H8"/>
                  <path d="M10 9H8"/>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-800 mb-3">CSV加工ツール</h3>
              <p class="text-gray-600 mb-4">在庫データや価格リストを効率的に加工・分析</p>
              <div class="flex items-center text-green-600 group-hover:text-green-700 transition-colors">
                <span class="mr-2">ツールを開く</span>
                <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Features Section -->
      <div class="mt-16">
        <h3 class="text-2xl font-bold text-gray-800 text-center mb-8">主要機能</h3>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <h4 class="text-gray-800 font-semibold mb-2">高精度計算</h4>
            <p class="text-gray-600 text-sm">最新の市場価格を反映した正確な算出</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13 9h-2v2h2V9zm0 4h-2v6h2v-6zm-1-9C6.48 4 2 8.48 2 14s4.48 10 10 10 10-4.48 10-10S17.52 4 12 4z"/>
              </svg>
            </div>
            <h4 class="text-gray-800 font-semibold mb-2">直感的操作</h4>
            <p class="text-gray-600 text-sm">シンプルで使いやすいインターフェース</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-gradient-to-r from-red-500 to-red-600 rounded-lg flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
              </svg>
            </div>
            <h4 class="text-gray-800 font-semibold mb-2">リアルタイム更新</h4>
            <p class="text-gray-600 text-sm">市場の変動に即座対応した価格情報</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { removeToken } from '@/utils/auth.js'

export default {
  name: 'MainMenu',
  setup() {
    const router = useRouter()
    
    const handleLogout = () => {
      removeToken()
      router.push('/login')
    }
    
    return {
      handleLogout
    }
  }
}
</script>

<style scoped>
.menu-card {
  animation: slideInUp 0.6s ease-out forwards;
}

.menu-card:nth-child(1) {
  animation-delay: 0.1s;
}

.menu-card:nth-child(2) {
  animation-delay: 0.2s;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-inner {
  transform: translateZ(0);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-inner:hover {
  transform: translateY(-4px) scale(1.02);
}

.logout-btn {
  transition: all 0.2s ease;
}

.logout-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.pattern-bg {
  opacity: 0.2;
  background-image: radial-gradient(circle at 20px 20px, rgba(255, 255, 255, 0.1) 2px, transparent 2px);
  background-size: 40px 40px;
}

@media (max-width: 768px) {
  .menu-card {
    animation-delay: 0s;
  }
  
  .card-inner {
    padding: 1.5rem;
  }
  
  .grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>