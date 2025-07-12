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
      <div class="max-w-4xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-4">
            <button 
              @click="goBack"
              class="p-2 hover:bg-white/20 rounded-lg transition-colors"
            >
              <svg class="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-3xl font-bold text-gray-800 tracking-wide">アイテム詳細</h1>
              <p class="text-gray-600">{{ itemData.box_id || '-' }} - {{ itemData.box_no || '-' }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button 
              @click="toggleEdit"
              class="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 rounded-lg transition-colors border border-blue-200 hover:border-blue-300"
            >
              {{ isEditing ? 'キャンセル' : '編集' }}
            </button>
            <button 
              v-if="isEditing"
              @click="saveChanges"
              class="px-4 py-2 bg-green-50 hover:bg-green-100 text-green-600 hover:text-green-700 rounded-lg transition-colors border border-green-200 hover:border-green-300"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 max-w-4xl mx-auto px-6 pb-12">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span class="ml-2 text-gray-600">アイテム詳細を読み込み中...</span>
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

      <!-- Item Details -->
      <div v-else-if="itemData" class="space-y-6">
        <!-- Primary Information Card -->
        <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-6 shadow-lg">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">基本情報</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Box ID -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">箱番</label>
              <input 
                v-if="isEditing"
                v-model="editData.box_id"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.box_id || '-' }}</p>
            </div>

            <!-- Box Number -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">枝番</label>
              <input 
                v-if="isEditing"
                v-model="editData.box_no"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.box_no || '-' }}</p>
            </div>

            <!-- Material -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">素材</label>
              <input 
                v-if="isEditing"
                v-model="editData.material"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.material || '-' }}</p>
            </div>

            <!-- Total Weight -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">総重量</label>
              <input 
                v-if="isEditing"
                v-model="editData.weight"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.weight || '-' }}</p>
            </div>
          </div>
        </div>

        <!-- Price Information Card -->
        <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-6 shadow-lg">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">価格情報</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Jewelry Price -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">評価額</label>
              <input 
                v-if="isEditing"
                v-model="editData.jewelry_price"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="number"
                step="1"
              />
              <p v-else class="text-2xl font-bold text-green-600 bg-green-50 px-3 py-2 rounded-lg">
                ¥{{ formatPrice(itemData.jewelry_price) }}
              </p>
            </div>

            <!-- Material Price -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">素材価格</label>
              <input 
                v-if="isEditing"
                v-model="editData.material_price"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="number"
                step="1"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">
                ¥{{ formatPrice(itemData.material_price) }}
              </p>
            </div>

            <!-- Material Weight -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">地金重量</label>
              <input 
                v-if="isEditing"
                v-model="editData.material_weight"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="number"
                step="0.1"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">
                {{ formatWeight(itemData.material_weight) }}
              </p>
            </div>

            <!-- Gemstone Weight -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">宝石重量</label>
              <input 
                v-if="isEditing"
                v-model="editData.gemstone_weight"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="number"
                step="0.1"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">
                {{ formatWeight(itemData.gemstone_weight) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Additional Information Card -->
        <div class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-6 shadow-lg">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">詳細情報</h2>
          <div class="space-y-4">
            <!-- Miscellaneous -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">備考</label>
              <textarea 
                v-if="isEditing"
                v-model="editData.misc"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                rows="3"
              ></textarea>
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg min-h-[80px]">{{ itemData.misc || '-' }}</p>
            </div>

            <!-- Brand Name -->
            <div v-if="itemData.brand_name">
              <label class="block text-sm font-medium text-gray-700 mb-1">ブランド</label>
              <input 
                v-if="isEditing"
                v-model="editData.brand_name"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.brand_name || '-' }}</p>
            </div>

            <!-- Category -->
            <div v-if="itemData.subcategory_name">
              <label class="block text-sm font-medium text-gray-700 mb-1">品目</label>
              <input 
                v-if="isEditing"
                v-model="editData.subcategory_name"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.subcategory_name || '-' }}</p>
            </div>

            <!-- Accessories -->
            <div v-if="itemData.accessory_comment">
              <label class="block text-sm font-medium text-gray-700 mb-1">付属品</label>
              <input 
                v-if="isEditing"
                v-model="editData.accessory_comment"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 bg-white"
                type="text"
              />
              <p v-else class="text-gray-800 bg-gray-50 px-3 py-2 rounded-lg">{{ itemData.accessory_comment || '-' }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getToken } from '@/utils/auth.js'

export default {
  name: 'ItemDetailPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const itemData = ref({})
    const editData = reactive({})
    const isLoading = ref(false)
    const error = ref('')
    const isEditing = ref(false)

    const historyId = computed(() => route.params.historyId)
    const itemIndex = computed(() => parseInt(route.params.itemIndex))

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
        Object.assign(editData, itemData.value)
        isEditing.value = false
      } else {
        // Start editing - copy current data
        isEditing.value = true
        await nextTick()
        Object.assign(editData, itemData.value)
        console.log('Edit data:', editData)
        console.log('Item data:', itemData.value)
      }
    }

    const saveChanges = async () => {
      try {
        const token = getToken()
        const response = await fetch(`/api/calculation-history/${historyId.value}/item/${itemIndex.value}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(editData)
        })

        if (response.ok) {
          itemData.value = { ...editData }
          isEditing.value = false
          alert('変更が保存されました')
        } else {
          throw new Error('保存に失敗しました')
        }
      } catch (err) {
        alert(err.message)
      }
    }

    const loadItemDetail = async () => {
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
          throw new Error('アイテム詳細の取得に失敗しました')
        }

        const data = await response.json()
        const items = data.calculation_data?.items || []
        
        if (itemIndex.value >= 0 && itemIndex.value < items.length) {
          itemData.value = items[itemIndex.value]
          Object.assign(editData, itemData.value)
        } else {
          throw new Error('アイテムが見つかりません')
        }
        
      } catch (err) {
        error.value = err.message
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      loadItemDetail()
    })

    return {
      itemData,
      editData,
      isLoading,
      error,
      isEditing,
      formatPrice,
      formatWeight,
      goBack,
      toggleEdit,
      saveChanges
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
}
</style>