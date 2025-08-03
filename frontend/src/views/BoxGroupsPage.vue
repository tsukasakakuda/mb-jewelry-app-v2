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
              <p class="text-gray-600" v-if="calculationName">{{ calculationName }} - 箱番号ごとに分類されたアイテム</p>
              <p class="text-gray-600" v-else>箱番号ごとに分類されたアイテム</p>
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
          <div v-for="(items, boxId) in boxGroups" :key="boxId" class="bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl p-6 shadow-lg">
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

            <!-- Items List -->
            <div class="bg-gray-50 rounded-lg overflow-hidden">
              <table class="w-full">
                <thead class="bg-gray-100 border-b border-gray-200">
                  <tr>
                    <!-- Row 1: Basic Info -->
                    <th class="text-left p-2 text-xs font-medium text-gray-600">商品情報</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">品目</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">ブランド</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">材質</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">重量</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600" colspan="2">備考</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">付属品</th>
                    <!-- Row 1: Detail Info -->
                    <th class="text-left p-2 text-xs font-medium text-gray-600">LIVE</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">RANK</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600" rowspan="2">操作</th>
                  </tr>
                  <tr>
                    <!-- Row 1: Basic Info -->
                    <th class="text-left p-2 text-xs font-medium text-gray-600">価格情報</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">予算下限</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">予算上限</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">予算予備</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">枠代金</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">脇代金</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">地金代金</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">地金単価</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">地金重量</th>
                    <th class="text-left p-2 text-xs font-medium text-gray-600">宝石重量</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(entry, index) in items" :key="index">
                    <!-- First Row -->
                    <tr class="border-b border-gray-200 hover:bg-gray-100 transition-colors duration-200">
                      <!-- Basic Info -->
                      <td class="p-2 text-gray-800 text-sm" rowspan="2">{{ entry.item.box_no || '-' }}</td>
                      <!-- 品目 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.subcategory_name"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.subcategory_name || '-' }}</span>
                      </td>
                      <!-- ブランド -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.brand_name"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.brand_name || '-' }}</span>
                      </td>
                      <!-- 素材 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.material"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.material || '-' }}</span>
                      </td>
                      <!-- 重量 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.weight"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.weight || '-' }}</span>
                      </td>
                      <!-- 備考 -->
                      <td class="p-1 text-gray-800 text-sm" colspan="2">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.misc"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.misc || '-' }}</span>
                      </td>
                      <!-- 付属品 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.accessory_comment"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.accessory_comment || '-' }}</span>
                      </td>
                      <!-- LIVE -->
                      <td class="p-1 text-gray-600 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.live"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.live || '-' }}</span>
                      </td>
                      <!-- RANK -->
                      <td class="p-1 text-gray-600 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model="editData.rank"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="text" />
                        <span v-else>{{ entry.item.rank || '-' }}</span>
                      </td>
                      <!-- Action Buttons -->
                      <td class="p-2 text-center" rowspan="2">
                        <div v-if="!isEditing(entry.item.id)" class="flex flex-col gap-1">
                          <button 
                            @click="startEdit(entry)"
                            class="px-2 py-1 bg-green-50 hover:bg-green-100 text-green-600 hover:text-green-700 rounded-md text-xs transition-colors border border-green-200 hover:border-green-300"
                          >
                            編集
                          </button>
                          <button 
                            @click="goToItemDetail(entry)"
                            class="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 rounded-md text-xs transition-colors border border-blue-200 hover:border-blue-300"
                          >
                            詳細
                          </button>
                        </div>
                        <div v-else class="flex flex-col gap-1">
                          <button 
                            @click="saveEdit"
                            class="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 rounded-md text-xs transition-colors border border-blue-200 hover:border-blue-300"
                          >
                            保存
                          </button>
                          <button 
                            @click="cancelEdit"
                            class="px-2 py-1 bg-gray-50 hover:bg-gray-100 text-gray-600 hover:text-gray-700 rounded-md text-xs transition-colors border border-gray-200 hover:border-gray-300"
                          >
                            取消
                          </button>
                        </div>
                      </td>
                    </tr>
                    <!-- Second Row -->
                    <tr class="border-b-2 border-gray-300 hover:bg-gray-100 transition-colors duration-200">
                      <!-- 予算下限 -->
                      <td class="p-1 text-gray-600 text-xs">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.budget_lower"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.budget_lower) }}</span>
                      </td>
                      <!-- 予算上限 -->
                      <td class="p-1 text-gray-600 text-xs">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.budget_upper"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.budget_upper) }}</span>
                      </td>
                      <!-- 予算予備 -->
                      <td class="p-1 text-gray-600 text-xs">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.budget_reserve"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.budget_reserve) }}</span>
                      </td>
                      <!-- 枠代金 -->
                      <td class="p-1 text-gray-600 text-xs">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.frame_price"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.frame_price) }}</span>
                      </td>
                      <!-- 脇代金 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.side_stone_price"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.side_stone_price) }}</span>
                      </td>
                      <!-- 地金代金 -->
                      <td class="p-1 text-gray-800 font-medium text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.jewelry_price"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.jewelry_price) }}</span>
                      </td>
                      <!-- 地金単価 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.material_price"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" />
                        <span v-else>{{ formatCurrency(entry.item.material_price) }}</span>
                      </td>
                      <!-- 地金重量 -->
                      <td class="p-1 text-gray-800 text-sm">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.material_weight"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" step="0.1" />
                        <span v-else>{{ formatWeight(entry.item.material_weight) }}</span>
                      </td>
                      <!-- 宝石重量 -->
                      <td class="p-1 text-gray-600 text-xs">
                        <input v-if="isEditing(entry.item.id)" 
                               v-model.number="editData.gemstone_weight"
                               class="w-full px-1 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                               type="number" step="0.1" />
                        <span v-else>{{ formatWeight(entry.item.gemstone_weight) }}</span>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
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
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { isAuthenticated, getToken } from '@/utils/auth.js'

export default {
  name: 'BoxGroupsPage',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const loading = ref(true)
    const error = ref('')
    const boxGroups = ref({})
    const historyId = ref(route.params.historyId)
    const calculationName = ref('')
    
    // 編集機能用の状態
    const editingItemId = ref(null)
    const editData = ref({})

    const fetchBoxGroups = async () => {
      try {
        loading.value = true
        error.value = ''
        
        if (!isAuthenticated()) {
          console.log('Not authenticated, redirecting to login')
          router.push('/login')
          return
        }

        if (!historyId.value) {
          error.value = '計算履歴IDが見つかりません'
          return
        }

        const token = getToken()

        console.log('Fetching box groups for history:', historyId.value)
        
        const response = await axios.get(`/api/calculation-history/${historyId.value}/box-groups`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        console.log('Box groups response:', response.data)
        console.log('First item details:', Object.values(response.data.box_groups || {})?.[0]?.[0]?.item)
        boxGroups.value = response.data.box_groups || {}
        
        // 計算名も取得
        if (Object.keys(boxGroups.value).length > 0) {
          const firstBox = Object.values(boxGroups.value)[0]
          if (firstBox && firstBox.length > 0) {
            calculationName.value = firstBox[0].calculation_name
          }
        }
        
      } catch (err) {
        console.error('箱番号グループ取得エラー:', err)
        console.error('Error response:', err.response)
        
        if (err.response?.status === 401) {
          console.log('Authentication failed, redirecting to login')
          localStorage.removeItem('token')
          router.push('/login')
        } else if (err.response?.status === 404) {
          error.value = '指定された計算履歴が見つかりません'
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

    const goToItemDetail = async (entry) => {
      try {
        if (!isAuthenticated()) {
          router.push('/login')
          return
        }

        console.log('Navigating to item detail for entry:', entry)

        // アイテムIDベースで詳細を取得してインデックスを特定
        const token = getToken()
        const response = await axios.get(`/api/calculation-history/${historyId.value}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.data && response.data.calculation_data && response.data.calculation_data.items) {
          const items = response.data.calculation_data.items
          
          // item_idで検索（最も確実）
          let itemIndex = items.findIndex(item => parseInt(item.id) === parseInt(entry.item.id))
          
          // item_idで見つからない場合は複合条件で検索
          if (itemIndex < 0) {
            itemIndex = items.findIndex(item => 
              item.box_id == entry.item.box_id && 
              item.box_no == entry.item.box_no &&
              item.material === entry.item.material &&
              item.weight === entry.item.weight
            )
          }

          if (itemIndex >= 0) {
            console.log(`Item found at index ${itemIndex}, navigating to detail page`)
            router.push(`/history/${historyId.value}/item/${itemIndex}`)
          } else {
            console.warn('Item not found in calculation history, falling back to history page')
            router.push(`/history/${historyId.value}`)
          }
        } else {
          console.error('No calculation data found, falling back to history page')
          router.push(`/history/${historyId.value}`)
        }
      } catch (err) {
        console.error('アイテム詳細遷移エラー:', err)
        // エラーの場合も計算履歴ページに遷移
        router.push(`/history/${historyId.value}`)
      }
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

    const formatWeight = (weight) => {
      if (!weight) return '0g'
      return `${parseFloat(weight).toFixed(1)}g`
    }

    // 編集機能
    const startEdit = (entry) => {
      editingItemId.value = entry.item.id
      editData.value = { ...entry.item }
      console.log('編集開始:', editData.value)
    }

    const cancelEdit = () => {
      editingItemId.value = null
      editData.value = {}
    }

    const saveEdit = async () => {
      try {
        const token = getToken()
        
        // フィールド名をデータベースに合わせてマッピング
        const mappedData = { ...editData.value }
        if (mappedData.weight !== undefined) {
          mappedData.weight_text = mappedData.weight
          delete mappedData.weight
        }
        
        // データベースに存在するフィールドのみを送信
        const dbFields = [
          'box_id', 'box_no', 'material', 'weight_text', 'weight_grams', 
          'jewelry_price', 'material_price', 'total_weight', 'gemstone_weight', 'material_weight', 'misc',
          'brand_name', 'subcategory_name', 'accessory_comment',
          'budget_lower', 'budget_upper', 'budget_reserve',
          'frame_price', 'side_stone_price', 'live', 'rank'
        ]
        const filteredData = {}
        for (const field of dbFields) {
          if (mappedData[field] !== undefined) {
            filteredData[field] = mappedData[field]
          }
        }

        console.log('Saving data:', filteredData)

        // アイテムインデックスを取得（詳細画面での更新と同じAPI）
        const historyResponse = await axios.get(`/api/calculation-history/${historyId.value}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        const items = historyResponse.data.calculation_data.items
        let itemIndex = items.findIndex(item => parseInt(item.id) === parseInt(editingItemId.value))

        if (itemIndex >= 0) {
          const response = await axios.put(`/api/calculation-history/${historyId.value}/item/${itemIndex}`, 
            filteredData, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })

          if (response.status === 200) {
            // データを更新
            Object.assign(editData.value, filteredData)
            
            // 箱グループデータを再取得
            await fetchBoxGroups()
            
            editingItemId.value = null
            editData.value = {}
            alert('変更が保存されました')
          } else {
            throw new Error('保存に失敗しました')
          }
        } else {
          throw new Error('アイテムが見つかりません')
        }
      } catch (err) {
        console.error('保存エラー:', err)
        alert(err.message || '保存中にエラーが発生しました')
      }
    }

    const isEditing = (itemId) => {
      return editingItemId.value === itemId
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
      historyId,
      calculationName,
      editingItemId,
      editData,
      goToHistory,
      goToItemDetail,
      formatDate,
      formatCurrency,
      formatWeight,
      startEdit,
      cancelEdit,
      saveEdit,
      isEditing
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