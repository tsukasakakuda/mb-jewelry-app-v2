export const getToken = () => {
  return localStorage.getItem('token') || sessionStorage.getItem('token')
}

export const setToken = (token, remember = false) => {
  if (remember) {
    localStorage.setItem('token', token)
    sessionStorage.removeItem('token')
  } else {
    sessionStorage.setItem('token', token)
    localStorage.removeItem('token')
  }
}

export const removeToken = () => {
  localStorage.removeItem('token')
  sessionStorage.removeItem('token')
}

export const isAuthenticated = () => {
  const token = getToken()
  if (!token) return false
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Date.now() / 1000
    console.log('Token payload:', payload)
    console.log('Current time:', currentTime)
    console.log('Token exp:', payload.exp)
    console.log('Is valid:', payload.exp > currentTime)
    return payload.exp > currentTime
  } catch (error) {
    console.error('Token validation error:', error)
    return false
  }
}

export const getUserInfo = () => {
  const token = getToken()
  if (!token) return null
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      id: payload.user_id || payload.sub,
      username: payload.username || payload.sub,
      role: payload.role,
      exp: payload.exp
    }
  } catch (error) {
    return null
  }
}

export const isAdmin = () => {
  const userInfo = getUserInfo()
  return userInfo && userInfo.role === 'admin'
}

export const createAuthHeader = () => {
  const token = getToken()
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

export const redirectToLogin = () => {
  removeToken()
  window.location.href = '/login'
}