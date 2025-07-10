<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div class="absolute inset-0 login-pattern-bg"></div>
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full opacity-20 blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full opacity-15 blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Login Card -->
    <div class="relative z-10 w-full max-w-md mx-4">
      <div class="login-card backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8 transition-all duration-300 hover:shadow-3xl hover:bg-white/15">
        <!-- Logo/Brand -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full mb-4 shadow-lg">
            <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm3.5 6L12 10.5 8.5 8 12 5.5 15.5 8zM12 21.5c-5.24 0-9.5-4.26-9.5-9.5S6.76 2.5 12 2.5s9.5 4.26 9.5 9.5-4.26 9.5-9.5 9.5z"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-white mb-2 tracking-wide">MB Jewelry</h1>
          <p class="text-white/70 text-sm">プロフェッショナルツールへようこそ</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Username Field -->
          <div class="floating-label-group">
            <input
              id="username"
              v-model="username"
              type="text"
              required
              :class="['floating-label-input', { 'has-content': username }]"
              @focus="focusField('username')"
              @blur="blurField('username')"
            />
            <label for="username" class="floating-label">ユーザー名</label>
            <div class="input-border"></div>
          </div>

          <!-- Password Field -->
          <div class="floating-label-group">
            <input
              id="password"
              v-model="password"
              type="password"
              required
              :class="['floating-label-input', { 'has-content': password }]"
              @focus="focusField('password')"
              @blur="blurField('password')"
            />
            <label for="password" class="floating-label">パスワード</label>
            <div class="input-border"></div>
          </div>

          <!-- Remember Me -->
          <div class="flex items-center justify-between">
            <label class="flex items-center cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="sr-only"
              />
              <div class="custom-checkbox">
                <svg v-if="rememberMe" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
              </div>
              <span class="ml-2 text-sm text-white/80">ログイン状態を保持する</span>
            </label>
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="login-button w-full py-3 px-4 rounded-xl font-medium text-white bg-gradient-to-r from-yellow-400 to-orange-500 hover:from-yellow-500 hover:to-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl"
          >
            <span v-if="isLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              ログイン中...
            </span>
            <span v-else>ログイン</span>
          </button>

          <!-- Error Message -->
          <div v-if="errorMessage" class="error-message">
            <div class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <span class="text-red-100 text-sm">{{ errorMessage }}</span>
            </div>
          </div>
        </form>
      </div>
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
    const focusedField = ref('')

    const focusField = (fieldName) => {
      focusedField.value = fieldName
    }

    const blurField = (fieldName) => {
      if (focusedField.value === fieldName) {
        focusedField.value = ''
      }
    }

    const handleLogin = async () => {
      if (!username.value || !password.value) {
        errorMessage.value = 'ユーザー名とパスワードを入力してください'
        return
      }

      isLoading.value = true
      errorMessage.value = ''

      console.log('Login attempt:', { username: username.value, password: password.value })

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

        console.log('Response status:', response.status)
        console.log('Response headers:', response.headers)

        if (response.ok) {
          const data = await response.json()
          console.log('Login success:', data)
          
          if (rememberMe.value) {
            localStorage.setItem('token', data.token)
            sessionStorage.removeItem('token')
          } else {
            sessionStorage.setItem('token', data.token)
            localStorage.removeItem('token')
          }
          
          console.log('Token stored, navigating to home...')
          console.log('Stored token:', localStorage.getItem('token') || sessionStorage.getItem('token'))
          
          // 強制的にページをリロードして認証状態を更新
          window.location.href = '/'
        } else {
          const error = await response.json()
          console.log('Login error:', error)
          errorMessage.value = error.message || 'ログインに失敗しました'
        }
      } catch (error) {
        console.error('Network error:', error)
        errorMessage.value = 'ネットワークエラーが発生しました: ' + error.message
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
      focusedField,
      focusField,
      blurField,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-card {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.floating-label-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.floating-label-input {
  width: 100%;
  padding: 12px 16px 12px 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.floating-label-input:focus {
  border-color: rgba(255, 193, 7, 0.8);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.1);
}

.floating-label-input.has-content {
  padding-top: 20px;
  padding-bottom: 8px;
}

.floating-label {
  position: absolute;
  left: 16px;
  top: 14px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  transition: all 0.3s ease;
  pointer-events: none;
  transform-origin: left top;
}

.floating-label-input:focus + .floating-label,
.floating-label-input.has-content + .floating-label {
  transform: translateY(-8px) scale(0.75);
  color: rgba(255, 193, 7, 0.9);
}

.floating-label-input::placeholder {
  color: transparent;
}

.floating-label-input:focus::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.custom-checkbox {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
}

.custom-checkbox:hover {
  border-color: rgba(255, 193, 7, 0.6);
  background: rgba(255, 193, 7, 0.1);
}

input[type="checkbox"]:checked + .custom-checkbox {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-color: #f59e0b;
}

.login-button {
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-button:hover::before {
  left: 100%;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-top: 16px;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.login-pattern-bg {
  opacity: 0.3;
  background-image: radial-gradient(circle at 30px 30px, rgba(255, 255, 255, 0.05) 2px, transparent 2px);
  background-size: 60px 60px;
}

@media (max-width: 768px) {
  .login-card {
    margin: 1rem;
    padding: 1.5rem;
  }
}
</style>