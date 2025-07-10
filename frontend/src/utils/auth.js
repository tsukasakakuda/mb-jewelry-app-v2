export const getToken = () => {
  return localStorage.getItem('token') || sessionStorage.getItem('token')
}

export const setToken = (token, remember = false) => {
  if (remember) {
    localStorage.setItem('token', token)
  } else {
    sessionStorage.setItem('token', token)
  }
}

export const removeToken = () => {
  localStorage.removeItem('token')
  sessionStorage.removeItem('token')
}

export const isAuthenticated = () => {
  return !!getToken()
}

export const createAuthHeader = () => {
  const token = getToken()
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}