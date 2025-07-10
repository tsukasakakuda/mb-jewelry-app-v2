<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          ログイン
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">ユーザー名</label>
            <input
              id="username"
              v-model="username"
              name="username"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="ユーザー名"
            />
          </div>
          <div>
            <label for="password" class="sr-only">パスワード</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="パスワード"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              v-model="rememberMe"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              ログイン状態を保持する
            </label>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            <span v-if="isLoading">ログイン中...</span>
            <span v-else>ログイン</span>
          </button>
        </div>

        <div v-if="errorMessage" class="mt-4 text-center text-red-600">
          {{ errorMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const isLoading = ref(false)
    const errorMessage = ref('')

    const handleLogin = async () => {
      if (!username.value || !password.value) {
        errorMessage.value = 'ユーザー名とパスワードを入力してください'
        return
      }

      isLoading.value = true
      errorMessage.value = ''

      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
          }),
        })

        if (response.ok) {
          const data = await response.json()
          
          if (rememberMe.value) {
            localStorage.setItem('token', data.token)
          } else {
            sessionStorage.setItem('token', data.token)
          }
          
          router.push('/')
        } else {
          const error = await response.json()
          errorMessage.value = error.message || 'ログインに失敗しました'
        }
      } catch (error) {
        errorMessage.value = 'ネットワークエラーが発生しました'
      } finally {
        isLoading.value = false
      }
    }

    return {
      username,
      password,
      rememberMe,
      isLoading,
      errorMessage,
      handleLogin
    }
  }
}
</script>