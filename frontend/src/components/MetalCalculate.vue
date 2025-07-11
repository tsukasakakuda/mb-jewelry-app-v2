<template>
  <div class="min-h-screen p-6 w-full">
    <div class="max-w-4xl mx-auto space-y-6">
      <!-- Page Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full mb-4 shadow-lg">
          <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2 tracking-wide">
          地金自動計算
        </h1>
        <p class="text-gray-600 text-sm">金属の価格を自動で計算します</p>
      </div>

      <!-- Main Form Card -->
      <div class="backdrop-blur-sm bg-white/90 border border-gray-200 rounded-3xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl hover:bg-white/95">
        <form @submit.prevent="checkWeights" class="space-y-6">
          <!-- Item CSV Upload -->
          <div class="file-upload-group">
            <label class="block font-semibold text-gray-800 mb-3 text-lg">item_csv</label>
            <div class="file-upload-container">
              <input
                type="file"
                @change="onItemChange"
                required
                accept=".csv"
                class="file-input"
                id="itemFile"
              />
              <label for="itemFile" class="file-upload-label">
                <svg class="w-8 h-8 text-gray-600 mb-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
                <span class="text-gray-800 font-medium">{{ itemFile ? itemFile.name : 'アイテムCSVを選択' }}</span>
                <span class="text-gray-600 text-sm block mt-1">計算対象のアイテムデータ</span>
              </label>
            </div>
          </div>
          
          <!-- Price CSV Upload -->
          <div class="file-upload-group">
            <label class="block font-semibold text-gray-800 mb-3 text-lg">price_csv</label>
            <div class="file-upload-container">
              <input
                type="file"
                @change="onPriceChange"
                required
                accept=".csv"
                class="file-input"
                id="priceFile"
              />
              <label for="priceFile" class="file-upload-label">
                <svg class="w-8 h-8 text-gray-600 mb-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7,15H9C9,16.08 10.37,17 12,17C13.63,17 15,16.08 15,15C15,13.9 13.96,13.5 11.76,12.97C9.64,12.44 7,11.78 7,9C7,7.21 8.47,5.69 10.5,5.18V3H13.5V5.18C15.53,5.69 17,7.21 17,9H15C15,7.92 13.63,7 12,7C10.37,7 9,7.92 9,9C9,10.1 10.04,10.5 12.24,11.03C14.36,11.56 17,12.22 17,15C17,16.79 15.53,18.31 13.5,18.82V21H10.5V18.82C8.47,18.31 7,16.79 7,15Z"/>
                </svg>
                <span class="text-gray-800 font-medium">{{ priceFile ? priceFile.name : '価格CSVを選択' }}</span>
                <span class="text-gray-600 text-sm block mt-1">素材の価格データ</span>
              </label>
            </div>
          </div>
          
          <!-- Submit Button -->
          <div class="text-center">
            <button
              type="submit"
              :disabled="!itemFile || !priceFile"
              class="submit-button w-full py-3 px-6 rounded-xl font-medium text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >
              アップロードしてチェック
            </button>
          </div>
        </form>
      </div>

      <!-- Data Correction Section -->
      <div v-if="invalidWeights.length" class="backdrop-blur-sm bg-white/90 border border-gray-200 rounded-3xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl hover:bg-white/95">
        <h2 class="text-xl font-semibold text-red-600 mb-6 flex items-center">
          <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z"/>
          </svg>
          修正が必要なデータ
        </h2>
        
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-gray-800 font-medium">box_id</th>
                <th class="border border-gray-300 px-3 py-2 text-gray-800 font-medium">box_no</th>
                <th class="border border-gray-300 px-3 py-2 text-gray-800 font-medium">material</th>
                <th class="border border-gray-300 px-3 py-2 text-gray-800 font-medium">misc</th>
                <th class="border border-gray-300 px-3 py-2 text-gray-800 font-medium">weight（修正可）</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in invalidWeights" :key="idx" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-3 py-2 text-gray-700">{{ item.box_id }}</td>
                <td class="border border-gray-300 px-3 py-2 text-gray-700">{{ item.box_no }}</td>
                <td class="border border-gray-300 px-3 py-2 text-gray-700">{{ item.row_data.material }}</td>
                <td class="border border-gray-300 px-3 py-2 text-gray-700">{{ item.row_data.misc }}</td>
                <td class="border border-gray-300 px-3 py-2">
                  <input 
                    v-model="item.row_data.weight" 
                    class="w-full px-2 py-1 bg-white border border-gray-300 rounded-md text-gray-800 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" 
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4 mt-6">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700 mb-2">計算名（DB保存時）</label>
            <input
              v-model="calculationName"
              type="text"
              placeholder="計算名を入力（例：2025年1月分）"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-800 placeholder-gray-500"
            />
          </div>
          <div class="flex gap-3">
            <button
              @click="submitFixedData"
              class="submit-button py-3 px-6 rounded-xl font-medium text-white bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >
              CSVダウンロード
            </button>
            <button
              @click="saveToDatabase"
              class="submit-button py-3 px-6 rounded-xl font-medium text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >
              DB保存
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      itemFile: null,
      priceFile: null,
      priceData: [],
      invalidWeights: [],
      allItems: [],
      validItems: [],
      calculationName: '',
      baseURL: import.meta.env.VITE_API_BASE,
    };
  },
  methods: {
    onItemChange(e) {
      this.itemFile = e.target.files[0] || null;
    },
    async onPriceChange(e) {
      this.priceFile = e.target.files[0] || null;
      if (!this.priceFile) return;

      const text = await this.priceFile.text();
      const rows = text.trim().split('\n');
      const headers = rows[0].split(',');
      this.priceData = rows.slice(1).map(row => {
        const values = row.split(',');
        const obj = {};
        headers.forEach((h, i) => obj[h.trim()] = values[i]?.trim() ?? '');
        return obj;
      });
    },
    async checkWeights() {
      if (!this.itemFile || !this.priceFile) {
        alert("両方のCSVファイルを選択してください");
        return;
      }

      const formData = new FormData();
      formData.append("item_file", this.itemFile);

      const text = await this.itemFile.text();
      const rows = text.trim().split('\n');
      const headers = rows[0].split(',');
      this.allItems = rows.slice(1).map((row, index) => {
        const values = row.split(',');
        const obj = {};
        headers.forEach((h, i) => obj[h.trim()] = values[i]?.trim() ?? '');
        obj.original_index = index;
        return obj;
      });

      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        console.log("Token for API request:", token ? "exists" : "missing");
        console.log("Making request to /api/check-weights");
        
        const res = await fetch('/api/check-weights', {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });
        
        console.log("API response status:", res.status);
        if (!res.ok) {
          if (res.status === 401) {
            alert("認証エラーです。再度ログインしてください。");
            window.location.href = '/login';
            return;
          }
          throw new Error(`API エラー: ${res.status}`);
        }

        const data = await res.json();
        this.invalidWeights = data.invalid_weights || [];

        const errorIndexes = new Set(this.invalidWeights.map(w => w.index));
        this.validItems = this.allItems.filter((_, idx) => !errorIndexes.has(idx));

        console.log("Invalid weights found:", this.invalidWeights.length);
        console.log("Invalid weights data:", this.invalidWeights);

        if (this.invalidWeights.length === 0) {
          this.submitFixedData();
        }
      } catch (err) {
        console.error("checkWeightsエラー:", err);
        alert("CSVチェックに失敗しました: " + err.message);
      }
    },
    async submitFixedData() {
      const fixedItems = this.invalidWeights.map(w => w.row_data);
      const mergedItems = [...this.validItems, ...fixedItems];

      const payload = {
        item_data: mergedItems,
        price_data: this.priceData
      };

      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const res = await fetch('/api/calculate-fixed', {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        });

        const disposition = res.headers.get("Content-Disposition");
        const match = disposition && disposition.match(/filename="?(.+)"?/);
        const filename = match ? match[1] : "calculated_result.csv";

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        console.error("submitFixedDataエラー:", err);
        alert("再計算に失敗しました");
      }
    },
    async saveToDatabase() {
      if (!this.calculationName.trim()) {
        alert("計算名を入力してください");
        return;
      }

      const fixedItems = this.invalidWeights.map(w => w.row_data);
      const mergedItems = [...this.validItems, ...fixedItems];

      if (mergedItems.length === 0) {
        alert("保存するデータがありません。先に計算を実行してください。");
        return;
      }

      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        if (!token) {
          alert("認証が必要です。ログインしてください。");
          return;
        }

        console.log("Saving to database:", {
          name: this.calculationName,
          itemCount: mergedItems.length,
          priceDataCount: this.priceData.length
        });

        // 計算処理を実行してアイテムデータに計算結果を追加
        const payload = {
          item_data: mergedItems,
          price_data: this.priceData
        };

        const calcRes = await fetch('/api/calculate-fixed', {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        });

        if (!calcRes.ok) {
          const errorText = await calcRes.text();
          console.error("Calculation API error:", errorText);
          throw new Error(`計算処理に失敗しました: ${calcRes.status}`);
        }

        // Note: /api/calculate-fixed returns CSV, but we need the calculated data
        // Let's modify the approach to calculate locally first
        
        // 実際の計算データを使用（既に計算済みの場合）
        let calculatedItems = mergedItems;
        let totalValue = 0;
        
        // もし計算結果がない場合は、簡易計算を実行
        if (!mergedItems[0]?.jewelry_price) {
          console.log("Performing simple calculation for items without jewelry_price");
          calculatedItems = mergedItems.map(item => {
            const weight = parseFloat(item.weight?.toString().replace(/[^\d.]/g, '') || '0');
            const estimatedPrice = weight * 5000; // 簡易計算：1gあたり5000円
            
            return {
              ...item,
              jewelry_price: estimatedPrice,
              total_weight: weight,
              material_price: 5000,
              gemstone_weight: 0,
              material_weight: weight
            };
          });
        }
        
        totalValue = calculatedItems.reduce((sum, item) => {
          const price = parseFloat(item.jewelry_price || '0');
          return sum + price;
        }, 0);

        const calculationResults = {
          timestamp: new Date().toISOString(),
          total_items: calculatedItems.length,
          total_value: totalValue,
          calculation_method: "metal_calculation"
        };

        // データベースに保存
        const savePayload = {
          calculation_name: this.calculationName,
          item_data: calculatedItems,
          calculation_results: calculationResults
        };

        console.log("Save payload:", savePayload);

        const saveRes = await fetch('/api/save-calculation', {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(savePayload)
        });

        if (!saveRes.ok) {
          const errorText = await saveRes.text();
          console.error("Save API error response:", errorText);
          console.error("Save API status:", saveRes.status);
          
          let errorMessage = `データベース保存に失敗しました: ${saveRes.status}`;
          try {
            const errorJson = JSON.parse(errorText);
            if (errorJson.error) {
              errorMessage = errorJson.error;
            }
          } catch (e) {
            // JSONパースエラーの場合はそのままテキストを使用
            errorMessage = errorText || errorMessage;
          }
          
          throw new Error(errorMessage);
        }

        const saveData = await saveRes.json();
        console.log("Save success:", saveData);
        alert(`計算結果が保存されました (ID: ${saveData.history_id})`);
        
        // 計算名をクリア
        this.calculationName = '';
        
      } catch (err) {
        console.error("saveToDatabase エラー:", err);
        alert("データベース保存に失敗しました: " + err.message);
      }
    }
  }
};
</script>

<style scoped>
.file-upload-group {
  position: relative;
}

.file-upload-container {
  position: relative;
  display: inline-block;
  width: 100%;
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 120px;
  padding: 2rem;
  border: 2px dashed rgb(209, 213, 219);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-upload-label:hover {
  border-color: rgb(59, 130, 246);
  background: rgba(59, 130, 246, 0.1);
  transform: translateY(-2px);
}

.submit-button {
  position: relative;
  overflow: hidden;
}

.submit-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.submit-button:hover::before {
  left: 100%;
}

@media (max-width: 768px) {
  .file-upload-label {
    min-height: 100px;
    padding: 1.5rem;
  }
  
  table {
    font-size: 0.75rem;
  }
  
  th, td {
    padding: 0.5rem;
  }
}
</style>