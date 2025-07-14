<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 relative overflow-hidden">
    <!-- Background Animation -->
    <div class="absolute inset-0">
      <div class="absolute top-0 left-0 w-full h-full pattern-bg"></div>
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-red-400/10 to-red-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 left-1/4 w-80 h-80 bg-gradient-to-r from-blue-400/10 to-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Header -->
    <header class="relative z-10 px-6 py-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-gradient-to-r from-red-500 to-red-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-3xl font-bold text-gray-800 tracking-wide">計算履歴</h1>
              <p class="text-gray-600">過去の計算結果を確認・管理・再利用</p>
            </div>
          </div>
          
          <router-link 
            to="/history/box-groups" 
            class="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
            <span>箱番号別表示</span>
          </router-link>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-4">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"/>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-gray-600">総計算数</p>
                <p class="text-lg font-semibold text-gray-800">{{ stats.total_calculations || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-4">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-gray-600">総アイテム数</p>
                <p class="text-lg font-semibold text-gray-800">{{ stats.total_items || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-4">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-gray-600">総評価額</p>
                <p class="text-lg font-semibold text-gray-800">¥{{ formatPrice(stats.total_value || 0) }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-4">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"/>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-gray-600">最終計算</p>
                <p class="text-lg font-semibold text-gray-800">{{ formatDate(stats.last_calculation) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 max-w-7xl mx-auto px-6 pb-12">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500"></div>
        <span class="ml-2 text-gray-600">計算履歴を読み込み中...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"/>
          </svg>
          <span class="ml-2 text-red-700">{{ error }}</span>
        </div>
      </div>

      <!-- History List -->
      <div v-else-if="histories.length > 0" class="space-y-4">
        <div v-for="history in histories" :key="history.id" 
             class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-6 hover:bg-white/90 transition-all duration-200 hover:shadow-lg">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-800 mb-1">{{ history.calculation_name }}</h3>
              <div class="flex items-center space-x-4 text-sm text-gray-600">
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"/>
                  </svg>
                  {{ history.item_count }}件
                </span>
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  ¥{{ formatPrice(history.total_value) }}
                </span>
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"/>
                  </svg>
                  {{ formatDate(history.created_at) }}
                </span>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="viewDetail(history.id)"
                class="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 rounded-lg transition-colors border border-blue-200 hover:border-blue-300"
              >
                詳細
              </button>
              <button 
                @click="viewSpreadsheet(history.id)"
                class="px-4 py-2 bg-purple-50 hover:bg-purple-100 text-purple-600 hover:text-purple-700 rounded-lg transition-colors border border-purple-200 hover:border-purple-300"
              >
                表計算
              </button>
              <button 
                @click="exportToCsv(history.id)"
                class="px-4 py-2 bg-green-50 hover:bg-green-100 text-green-600 hover:text-green-700 rounded-lg transition-colors border border-green-200 hover:border-green-300"
              >
                CSV
              </button>
              <button 
                @click="deleteHistory(history.id)"
                class="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 hover:text-red-700 rounded-lg transition-colors border border-red-200 hover:border-red-300"
              >
                削除
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"/>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-800 mb-2">計算履歴がありません</h3>
        <p class="text-gray-600 mb-4">地金計算を実行して結果を保存してください</p>
        <router-link 
          to="/calculate" 
          class="inline-flex items-center px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 rounded-lg transition-colors border border-blue-200 hover:border-blue-300"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"/>
          </svg>
          計算を開始
        </router-link>
      </div>
    </main>

    <!-- Detail Modal -->
    <div v-if="showDetailModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        <!-- Modal Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-semibold text-gray-800">{{ selectedDetail?.calculation_name }}</h3>
            <p class="text-gray-600 text-sm">{{ formatDate(selectedDetail?.created_at) }}</p>
          </div>
          <button 
            @click="closeDetailModal"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <!-- Modal Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          <!-- Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"/>
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm text-blue-600">総アイテム数</p>
                  <p class="text-lg font-semibold text-blue-800">{{ selectedDetail?.item_count }}</p>
                </div>
              </div>
            </div>

            <div class="bg-green-50 border border-green-200 rounded-lg p-4">
              <div class="flex items-center">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm text-green-600">総評価額</p>
                  <p class="text-lg font-semibold text-green-800">¥{{ formatPrice(selectedDetail?.total_value) }}</p>
                </div>
              </div>
            </div>

            <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <div class="flex items-center">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 4a1 1 0 011-1h1V2a1 1 0 012 0v1h2V2a1 1 0 012 0v1h2V2a1 1 0 012 0v1h1a1 1 0 011 1v1H3V4z"/>
                    <path fill-rule="evenodd" d="M3 6h14v10a2 2 0 01-2 2H5a2 2 0 01-2-2V6zm2 3a1 1 0 000 2h6a1 1 0 100-2H5z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm text-purple-600">総重量</p>
                  <p class="text-lg font-semibold text-purple-800">{{ formatWeight(selectedDetail?.calculation_data?.summary?.total_weight) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Item Details Table -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-4">アイテム詳細</h4>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="bg-gray-100">
                    <th class="text-left p-3 font-medium text-gray-700">箱ID</th>
                    <th class="text-left p-3 font-medium text-gray-700">枝番</th>
                    <th class="text-left p-3 font-medium text-gray-700">素材</th>
                    <th class="text-left p-3 font-medium text-gray-700">重量</th>
                    <th class="text-left p-3 font-medium text-gray-700">評価額</th>
                    <th class="text-left p-3 font-medium text-gray-700">備考</th>
                    <th class="text-left p-3 font-medium text-gray-700">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="(item, index) in selectedDetail?.calculation_data?.items" 
                    :key="index"
                    class="border-t border-gray-200 hover:bg-gray-50"
                  >
                    <td class="p-3 text-gray-800">{{ item.box_id || '-' }}</td>
                    <td class="p-3 text-gray-800">{{ item.box_no || '-' }}</td>
                    <td class="p-3 text-gray-800">{{ item.material || '-' }}</td>
                    <td class="p-3 text-gray-800">{{ item.weight || '-' }}</td>
                    <td class="p-3 text-gray-800 font-medium">¥{{ formatPrice(item.jewelry_price) }}</td>
                    <td class="p-3 text-gray-600 text-xs max-w-xs truncate">{{ item.misc || '-' }}</td>
                    <td class="p-3">
                      <button 
                        @click="viewItemDetail(selectedDetail.id, index)"
                        class="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 rounded text-xs transition-colors border border-blue-200 hover:border-blue-300"
                      >
                        詳細
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-3 mt-6">
            <button 
              @click="exportToCsv(selectedDetail.id)"
              class="px-4 py-2 bg-green-50 hover:bg-green-100 text-green-600 hover:text-green-700 rounded-lg transition-colors border border-green-200 hover:border-green-300"
            >
              CSVエクスポート
            </button>
            <button 
              @click="closeDetailModal"
              class="px-4 py-2 bg-gray-50 hover:bg-gray-100 text-gray-600 hover:text-gray-700 rounded-lg transition-colors border border-gray-200 hover:border-gray-300"
            >
              閉じる
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getToken } from '@/utils/auth.js'

export default {
  name: 'CalculationHistoryPage',
  setup() {
    const router = useRouter()
    const histories = ref([])
    const stats = ref({})
    const isLoading = ref(false)
    const error = ref('')
    const showDetailModal = ref(false)
    const selectedDetail = ref(null)

    const formatPrice = (value) => {
      if (!value) return '0'
      return new Intl.NumberFormat('ja-JP').format(Math.round(value))
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatWeight = (weight) => {
      if (!weight) return '0g'
      return `${parseFloat(weight).toFixed(1)}g`
    }

    const loadHistories = async () => {
      isLoading.value = true
      error.value = ''
      
      try {
        const token = getToken()
        if (!token) {
          throw new Error('認証が必要です')
        }

        const response = await fetch('/api/calculation-history', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) {
          throw new Error('履歴の取得に失敗しました')
        }

        const data = await response.json()
        histories.value = data.histories || []
        
      } catch (err) {
        error.value = err.message
      } finally {
        isLoading.value = false
      }
    }

    const loadStats = async () => {
      try {
        const token = getToken()
        if (!token) return

        const response = await fetch('/api/calculation-stats', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const data = await response.json()
          stats.value = data
        }
      } catch (err) {
        console.error('統計情報の取得に失敗:', err)
      }
    }

    const viewDetail = async (historyId) => {
      try {
        const token = getToken()
        const response = await fetch(`/api/calculation-history/${historyId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const detail = await response.json()
          selectedDetail.value = detail
          showDetailModal.value = true
        } else {
          throw new Error('詳細情報の取得に失敗しました')
        }
      } catch (err) {
        alert(err.message || '詳細情報の取得に失敗しました')
      }
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedDetail.value = null
    }

    const exportToCsv = async (historyId) => {
      try {
        const token = getToken()
        const response = await fetch(`/api/export-calculation/${historyId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `calculation_${historyId}.csv`
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
          window.URL.revokeObjectURL(url)
        } else {
          throw new Error('CSVエクスポートに失敗しました')
        }
      } catch (err) {
        alert(err.message)
      }
    }

    const viewItemDetail = (historyId, itemIndex) => {
      router.push(`/history/${historyId}/item/${itemIndex}`)
    }

    const viewSpreadsheet = (historyId) => {
      router.push(`/history/${historyId}/spreadsheet`)
    }

    const deleteHistory = async (historyId) => {
      if (!confirm('この計算履歴を削除しますか？')) return

      try {
        const token = getToken()
        const response = await fetch(`/api/calculation-history/${historyId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          histories.value = histories.value.filter(h => h.id !== historyId)
          await loadStats() // 統計情報を更新
        } else {
          throw new Error('削除に失敗しました')
        }
      } catch (err) {
        alert(err.message)
      }
    }

    onMounted(() => {
      loadHistories()
      loadStats()
    })

    return {
      histories,
      stats,
      isLoading,
      error,
      showDetailModal,
      selectedDetail,
      formatPrice,
      formatDate,
      formatWeight,
      viewDetail,
      closeDetailModal,
      exportToCsv,
      viewItemDetail,
      viewSpreadsheet,
      deleteHistory
    }
  }
}
</script>

<style scoped>
.pattern-bg {
  opacity: 0.2;
  background-image: radial-gradient(circle at 20px 20px, rgba(255, 255, 255, 0.1) 2px, transparent 2px);
  background-size: 40px 40px;
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
  
  /* Modal responsive styles */
  .max-w-6xl {
    max-width: 95vw;
  }
  
  .max-h-\[90vh\] {
    max-height: 95vh;
  }
  
  /* Table responsive */
  table {
    font-size: 0.75rem;
  }
  
  .max-w-xs {
    max-width: 100px;
  }
}

/* Modal animation */
.fixed.inset-0 {
  animation: fadeIn 0.2s ease-out;
}

.bg-white.rounded-xl {
  animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}
</style>