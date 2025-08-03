<template>
  <div class="min-h-screen p-6 w-full">
    <div class="max-w-2xl mx-auto space-y-6">
      <!-- Page Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-full mb-4 shadow-lg">
          <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2 tracking-wide">
          CSV 編集ツール
        </h1>
        <p class="text-gray-600 text-sm">データの編集と変換を行います</p>
      </div>

      <!-- Main Form Card -->
      <div class="backdrop-blur-sm bg-white/90 border border-gray-200 rounded-3xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl hover:bg-white/95">
        <form @submit.prevent="submitCsv" class="space-y-6">
          <!-- File Upload Section -->
          <div class="file-upload-group">
            <label class="block font-semibold text-gray-800 mb-3 text-lg">CSVファイル</label>
            <div class="file-upload-container">
              <input
                type="file"
                @change="onFileChange"
                required
                accept=".csv"
                class="file-input"
                id="csvFile"
              />
              <label for="csvFile" class="file-upload-label">
                <svg class="w-8 h-8 text-gray-600 mb-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
                <span class="text-gray-800 font-medium">{{ selectedFile ? selectedFile.name : 'ファイルを選択' }}</span>
                <span class="text-gray-600 text-sm block mt-1">CSVファイルをアップロード</span>
              </label>
            </div>
          </div>
          
          <!-- Submit Button -->
          <div class="text-center">
            <button
              type="submit"
              :disabled="!selectedFile"
              class="submit-button w-full py-3 px-6 rounded-xl font-medium text-white bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
            >
              編集してダウンロード
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      baseURL: import.meta.env.VITE_API_BASE
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0] || null;
    },
    async submitCsv() {
      if (!this.selectedFile) {
        alert("ファイルを選択してください");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const res = await fetch('/api/edit-csv', {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });

        if (!res.ok) {
          throw new Error("エラーが発生しました");
        }

        const disposition = res.headers.get("Content-Disposition");
        const match = disposition && disposition.match(/filename="?(.+)"?/);
        const filename = match ? match[1] : "edited_result.csv";

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        console.error("submitCsvエラー:", err);
        alert("CSV編集に失敗しました");
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
  border-color: rgb(34, 197, 94);
  background: rgba(34, 197, 94, 0.1);
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
}
</style>