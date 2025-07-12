<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button 
            @click="goBack"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
          <div>
            <h1 class="text-xl font-semibold text-gray-900">計算履歴詳細</h1>
            <p class="text-sm text-gray-500">{{ historyDetail?.date || '' }} - {{ historyDetail?.total_count || 0 }}件</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <button 
            @click="toggleEdit"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
              isEditing 
                ? 'bg-gray-100 text-gray-700 hover:bg-gray-200' 
                : 'bg-blue-600 text-white hover:bg-blue-700'
            ]"
          >
            {{ isEditing ? 'キャンセル' : '編集' }}
          </button>
          <button 
            v-if="isEditing"
            @click="saveChanges"
            class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            保存
          </button>
          <button 
            @click="exportToCSV"
            class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            CSV出力
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="p-6">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span class="ml-2 text-gray-600">データを読み込み中...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"/>
          </svg>
          <span class="ml-2 text-red-700">{{ error }}</span>
        </div>
      </div>

      <!-- Spreadsheet Table -->
      <div v-else-if="items.length > 0" class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full border-collapse">
            <!-- Header -->
            <thead class="bg-gray-50">
              <tr>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 w-12">#</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[120px]">箱番</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[80px]">枝番</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">素材</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">総重量</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[120px]">評価額</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">素材価格</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">地金重量</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">宝石重量</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[150px]">備考</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">ブランド</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 min-w-[100px]">品目</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[120px]">付属品</th>
              </tr>
            </thead>
            <!-- Body -->
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in items" :key="index" class="hover:bg-gray-50">
                <!-- Row Number -->
                <td class="px-3 py-2 text-sm text-gray-500 border-r border-gray-200 bg-gray-50 font-medium">{{ index + 1 }}</td>
                
                <!-- Box ID -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.box_id"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.box_id || '-' }}</span>
                </td>
                
                <!-- Box No -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.box_no"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.box_no || '-' }}</span>
                </td>
                
                <!-- Material -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.material"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.material || '-' }}</span>
                </td>
                
                <!-- Weight -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.weight"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.weight || '-' }}</span>
                </td>
                
                <!-- Jewelry Price -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.jewelry_price"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="number"
                    step="1"
                  />
                  <span v-else class="text-sm text-gray-900 font-medium text-green-600">¥{{ formatPrice(item.jewelry_price) }}</span>
                </td>
                
                <!-- Material Price -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.material_price"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="number"
                    step="1"
                  />
                  <span v-else class="text-sm text-gray-900">¥{{ formatPrice(item.material_price) }}</span>
                </td>
                
                <!-- Material Weight -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.material_weight"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="number"
                    step="0.1"
                  />
                  <span v-else class="text-sm text-gray-900">{{ formatWeight(item.material_weight) }}</span>
                </td>
                
                <!-- Gemstone Weight -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.gemstone_weight"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="number"
                    step="0.1"
                  />
                  <span v-else class="text-sm text-gray-900">{{ formatWeight(item.gemstone_weight) }}</span>
                </td>
                
                <!-- Misc -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.misc"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.misc || '-' }}</span>
                </td>
                
                <!-- Brand Name -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.brand_name"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.brand_name || '-' }}</span>
                </td>
                
                <!-- Subcategory Name -->
                <td class="px-3 py-2 border-r border-gray-200">
                  <input 
                    v-if="isEditing"
                    v-model="item.subcategory_name"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.subcategory_name || '-' }}</span>
                </td>
                
                <!-- Accessory Comment -->
                <td class="px-3 py-2">
                  <input 
                    v-if="isEditing"
                    v-model="item.accessory_comment"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    type="text"
                  />
                  <span v-else class="text-sm text-gray-900">{{ item.accessory_comment || '-' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Summary Footer -->
        <div class="bg-gray-50 border-t border-gray-200 px-6 py-4">
          <div class="flex justify-between items-center">
            <div class="text-sm text-gray-600">
              合計 {{ items.length }} 件
            </div>
            <div class="text-lg font-semibold text-gray-900">
              総評価額: ¥{{ formatPrice(totalJewelryPrice) }}
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getToken } from '@/utils/auth.js'

export default {
  name: 'SpreadsheetDetailPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const historyDetail = ref({})
    const items = ref([])
    const originalItems = ref([])
    const isLoading = ref(false)
    const error = ref('')
    const isEditing = ref(false)

    const historyId = computed(() => route.params.historyId)

    const totalJewelryPrice = computed(() => {
      return items.value.reduce((sum, item) => {
        return sum + (parseFloat(item.jewelry_price) || 0)
      }, 0)
    })

    const formatPrice = (value) => {
      if (!value) return '0'
      return new Intl.NumberFormat('ja-JP').format(Math.round(value))
    }

    const formatWeight = (weight) => {
      if (!weight) return '0g'
      return `${parseFloat(weight).toFixed(1)}g`
    }

    const goBack = () => {
      router.go(-1)
    }

    const toggleEdit = async () => {
      if (isEditing.value) {
        // Cancel editing - restore original data
        items.value = JSON.parse(JSON.stringify(originalItems.value))
        isEditing.value = false
      } else {
        // Start editing - backup current data
        originalItems.value = JSON.parse(JSON.stringify(items.value))
        isEditing.value = true
        await nextTick()
        console.log('Items before edit:', items.value)
        console.log('Original items:', originalItems.value)
      }
    }

    const saveChanges = async () => {
      try {
        const token = getToken()
        const response = await fetch(`/api/calculation-history/${historyId.value}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...historyDetail.value.calculation_data,
            items: items.value
          })
        })

        if (response.ok) {
          originalItems.value = JSON.parse(JSON.stringify(items.value))
          isEditing.value = false
          alert('変更が保存されました')
        } else {
          throw new Error('保存に失敗しました')
        }
      } catch (err) {
        alert(err.message)
      }
    }

    const exportToCSV = () => {
      // CSV export functionality (reuse existing logic)
      router.push(`/history/${historyId.value}/csv`)
    }

    const loadHistoryDetail = async () => {
      isLoading.value = true
      error.value = ''
      
      try {
        const token = getToken()
        if (!token) {
          throw new Error('認証が必要です')
        }

        const response = await fetch(`/api/calculation-history/${historyId.value}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) {
          throw new Error('履歴詳細の取得に失敗しました')
        }

        const data = await response.json()
        historyDetail.value = data
        items.value = data.calculation_data?.items || []
        originalItems.value = JSON.parse(JSON.stringify(items.value))
        
      } catch (err) {
        error.value = err.message
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      loadHistoryDetail()
    })

    return {
      historyDetail,
      items,
      isLoading,
      error,
      isEditing,
      totalJewelryPrice,
      formatPrice,
      formatWeight,
      goBack,
      toggleEdit,
      saveChanges,
      exportToCSV
    }
  }
}
</script>

<style scoped>
/* Spreadsheet-like styling */
table {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

th, td {
  border-right: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

th:last-child, td:last-child {
  border-right: none;
}

tr:hover {
  background-color: #f9fafb;
}

input:focus {
  z-index: 10;
  position: relative;
}

/* Fixed column widths for spreadsheet feel */
.min-w-\[120px\] { min-width: 120px; }
.min-w-\[80px\] { min-width: 80px; }
.min-w-\[100px\] { min-width: 100px; }
.min-w-\[150px\] { min-width: 150px; }

/* Sticky header */
thead th {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: #f9fafb;
}

/* Row number column styling */
td:first-child {
  background-color: #f9fafb;
  font-weight: 500;
  text-align: center;
}
</style>