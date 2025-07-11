<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">データベース内容確認</h1>
        <p class="text-gray-600">管理者専用 - データベースの全内容を表示</p>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span class="ml-2 text-gray-600">データベース内容を読み込み中...</span>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
        <span class="text-red-700">{{ error }}</span>
      </div>

      <!-- Database Content -->
      <div v-else-if="dbContent" class="space-y-6">
        <div class="bg-white rounded-xl p-4 shadow">
          <p class="text-sm text-gray-600 mb-2">データベースパス: {{ dbInfo.database_path }}</p>
          <p class="text-sm text-gray-600">テーブル数: {{ dbInfo.tables.length }}</p>
        </div>

        <!-- Tables -->
        <div v-for="table in dbInfo.tables" :key="table" class="bg-white rounded-xl shadow overflow-hidden">
          <div class="bg-gray-50 px-6 py-4 border-b">
            <h3 class="text-lg font-semibold text-gray-800">{{ table }}</h3>
            <p class="text-sm text-gray-600">レコード数: {{ dbContent[table]?.length || 0 }}</p>
          </div>
          
          <div v-if="dbContent[table]?.length" class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-100">
                <tr>
                  <th v-for="key in Object.keys(dbContent[table][0])" :key="key" 
                      class="text-left p-3 font-medium text-gray-700">
                    {{ key }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in dbContent[table]" :key="index" 
                    class="border-t hover:bg-gray-50">
                  <td v-for="key in Object.keys(row)" :key="key" class="p-3 text-gray-800">
                    <div v-if="key === 'calculation_data'" class="max-w-xs">
                      <details class="cursor-pointer">
                        <summary class="text-blue-600 hover:text-blue-800">JSON表示</summary>
                        <pre class="text-xs mt-2 bg-gray-100 p-2 rounded overflow-auto max-h-40">{{ formatJson(row[key]) }}</pre>
                      </details>
                    </div>
                    <span v-else class="max-w-xs block truncate">{{ row[key] }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="p-6 text-center text-gray-500">
            このテーブルにはデータがありません
          </div>
        </div>

        <!-- Refresh Button -->
        <div class="text-center">
          <button @click="loadDbContent" 
                  class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors">
            データを再読み込み
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { getToken } from '@/utils/auth.js'

export default {
  name: 'AdminDbView',
  setup() {
    const dbContent = ref(null)
    const dbInfo = ref(null)
    const isLoading = ref(false)
    const error = ref('')

    const formatJson = (jsonString) => {
      try {
        if (typeof jsonString === 'string') {
          return JSON.stringify(JSON.parse(jsonString), null, 2)
        }
        return JSON.stringify(jsonString, null, 2)
      } catch (e) {
        return jsonString
      }
    }

    const loadDbContent = async () => {
      isLoading.value = true
      error.value = ''
      
      try {
        const token = getToken()
        if (!token) {
          throw new Error('認証が必要です')
        }

        const response = await fetch('/api/admin/db-content', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) {
          if (response.status === 403) {
            throw new Error('管理者権限が必要です')
          }
          throw new Error('データベース内容の取得に失敗しました')
        }

        const data = await response.json()
        dbContent.value = data.content
        dbInfo.value = {
          tables: data.tables,
          database_path: data.database_path
        }
        
      } catch (err) {
        error.value = err.message
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      loadDbContent()
    })

    return {
      dbContent,
      dbInfo,
      isLoading,
      error,
      formatJson,
      loadDbContent
    }
  }
}
</script>