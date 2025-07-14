<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 relative overflow-hidden">
    <!-- Background Animation -->
    <div class="absolute inset-0">
      <div class="absolute top-0 left-0 w-full h-full pattern-bg"></div>
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-purple-400/10 to-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 left-1/4 w-80 h-80 bg-gradient-to-r from-pink-400/10 to-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Header -->
    <header class="relative z-10 px-6 py-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-3xl font-bold text-gray-800 tracking-wide">箱番号別グループ</h1>
              <p class="text-gray-600">箱番号ごとに分類された計算履歴</p>
            </div>
          </div>
          
          <router-link 
            to="/history" 
            class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200"
          >
            履歴一覧に戻る
          </router-link>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 px-6 pb-8">
      <div class="max-w-7xl mx-auto">
        
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">読み込み中...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
            <p class="text-red-600">{{ error }}</p>
          </div>
        </div>

        <!-- Box Groups -->
        <div v-else-if="boxGroups && Object.keys(boxGroups).length > 0" class="space-y-6">
          <div v-for="(items, boxId) in boxGroups" :key="boxId" 
               class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-6 shadow-lg">
            
            <!-- Box Header -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-purple-100 to-purple-200 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-semibold text-gray-800">箱番号: {{ boxId }}</h3>
                  <p class="text-sm text-gray-600">{{ items.length }}件のアイテム</p>
                </div>
              </div>
              
              <div class="text-right">
                <p class="text-sm text-gray-500">最大10件まで表示</p>
              </div>
            </div>

            <!-- Items Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="(entry, index) in items" :key="index" 
                   class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
                   @click="goToHistory(entry.history_id)">
                
                <!-- Item Info -->
                <div class="flex items-start justify-between mb-3">
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-800 mb-1">{{ entry.calculation_name }}</h4>
                    <p class="text-sm text-gray-600">{{ formatDate(entry.created_at) }}</p>
                  </div>
                  <div class="text-right">
                    <span class="text-xs bg-purple-100 text-purple-600 px-2 py-1 rounded">
                      ID: {{ entry.history_id }}
                    </span>
                  </div>
                </div>

                <!-- Item Details -->
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-500">材質:</span>
                    <span class="text-gray-700">{{ entry.item.material || 'N/A' }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-500">重量:</span>
                    <span class="text-gray-700">{{ entry.item.weight || 'N/A' }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-500">価格:</span>
                    <span class="text-gray-700 font-medium">
                      {{ formatCurrency(entry.item.jewelry_price) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-8 max-w-md mx-auto">
            <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
            </svg>
            <p class="text-gray-600">箱番号別のデータがありません</p>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { isAuthenticated, getToken } from '@/utils/auth.js'

export default {
  name: 'BoxGroupsPage',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const error = ref('')
    const boxGroups = ref({})

    const fetchBoxGroups = async () => {
      try {
        loading.value = true
        error.value = ''
        
        if (!isAuthenticated()) {
          console.log('Not authenticated, redirecting to login')
          router.push('/login')
          return
        }

        const token = getToken()

        console.log('Fetching box groups with token:', token.substring(0, 20) + '...')
        
        const response = await axios.get('/api/calculation-history/box-groups', {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          params: {
            max_per_box: 10
          }
        })

        console.log('Box groups response:', response.data)
        boxGroups.value = response.data.box_groups || {}
      } catch (err) {
        console.error('箱番号グループ取得エラー:', err)
        console.error('Error response:', err.response)
        
        if (err.response?.status === 401) {
          console.log('Authentication failed, redirecting to login')
          localStorage.removeItem('token')
          router.push('/login')
        } else {
          // 認証エラー以外の場合はページに留まり、エラーメッセージを表示
          error.value = err.response?.data?.error || '箱番号グループの取得に失敗しました'
        }
      } finally {
        loading.value = false
      }
    }

    const goToHistory = (historyId) => {
      router.push(`/history/${historyId}`)
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatCurrency = (amount) => {
      if (!amount) return '¥0'
      return new Intl.NumberFormat('ja-JP', {
        style: 'currency',
        currency: 'JPY',
        maximumFractionDigits: 0
      }).format(amount)
    }

    onMounted(() => {
      // 初期認証チェック
      if (!isAuthenticated()) {
        console.log('Not authenticated on mount, redirecting to login')
        router.push('/login')
        return
      }
      
      fetchBoxGroups()
    })

    return {
      loading,
      error,
      boxGroups,
      goToHistory,
      formatDate,
      formatCurrency
    }
  }
}
</script>

<style scoped>
.pattern-bg {
  background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.8) 1px, transparent 0);
  background-size: 20px 20px;
}
</style>