<template>
  <router-view />

  <div v-if="isSessionExpired" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 select-none">
    <div class="absolute inset-0 bg-slate-900/80 backdrop-blur-md"></div>
    <div class="relative bg-white w-full max-w-sm rounded-3xl shadow-2xl p-6 z-10 text-center border border-slate-100 animate-fade-in">
      <div class="mx-auto flex items-center justify-center h-14 w-14 rounded-full mb-4 shadow-inner bg-red-50 text-red-500 border border-red-100">
        <svg class="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      </div>
      <h3 class="text-lg font-black text-slate-900 mb-2">Session Expired</h3>
      <p class="text-sm text-slate-500 font-medium mb-8 leading-relaxed">Your session has timed out due to inactivity. Please log in again to secure your account.</p>
      <button @click="handleTimeoutLogout" class="w-full px-4 py-3 bg-red-600 hover:bg-red-700 text-white text-xs font-black uppercase tracking-wider rounded-xl transition-all shadow-md active:scale-95">
        Login Again
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const isSessionExpired = ref(false)
let sessionInterval = null
let lastSavedTime = 0
let isResetTriggered = false

// Sayacı sıfırlayan ana tetikleyici (Tıklamalarda anında sıfırlaması için force parametresi eklendi)
const resetSessionTimer = (force = false) => {
  if (window.__bonna_download_active || isSessionExpired.value) return
  const now = Date.now()
  
  if (force || (now - lastSavedTime > 1000)) {
    localStorage.setItem('loginTime', now.toString())
    lastSavedTime = now
    isResetTriggered = true
  }
}

// Saniyelik kontrol kronometresi ve Terminal Raporlama
const checkGlobalSession = async () => {
  const userSessionStr = localStorage.getItem('bonna_user_session')
  const loginTime = localStorage.getItem('loginTime')
  
  if (!userSessionStr || !loginTime) return
  const userSession = JSON.parse(userSessionStr)
  const email = userSession.email || 'System User'

  if (window.__bonna_download_active) {
    localStorage.setItem('loginTime', Date.now().toString())
    try {
      await axios.post(`${window.location.origin}/api/session/log`, {
        email: email,
        timePassedSeconds: 0,
        remainingSeconds: 60.0,
        status: "🛡️ IMMUNE (DOWNLOADING ACTIVE)"
      })
    } catch(e){}
    return
  }

  const timePassed = Date.now() - parseInt(loginTime)
  const expireLimit = 1 * 60 * 1000 // Test İçin 1 Dakika (Değişiklik onaylanınca burayı 180 yapabilirsin)
  
  const timePassedSeconds = timePassed / 1000
  const remainingSeconds = Math.max(0, (expireLimit - timePassed) / 1000)
  const currentState = isResetTriggered ? "🔴 TIMER RESET (USER ACTIVITY DETECTED)" : "🟢 COUNTING DOWN"
  isResetTriggered = false // Durumu sıfırla

  try {
    await axios.post(`${window.location.origin}/api/session/log`, {
      email: email,
      timePassedSeconds: timePassedSeconds,
      remainingSeconds: remainingSeconds,
      status: currentState
    })
  } catch (error) {}

  if (timePassed > expireLimit) {
    isSessionExpired.value = true
    clearInterval(sessionInterval)
    removeActivityListeners()
    try {
      await axios.post(`${window.location.origin}/api/session/log`, {
        email: email,
        timePassedSeconds: timePassedSeconds,
        remainingSeconds: 0,
        status: "🔒 LOCKDOWN - SESSION KILLED"
      })
    } catch (error) {}
  }
}

const handleTimeoutLogout = () => {
  localStorage.removeItem('bonna_user_session')
  localStorage.removeItem('loginTime')
  isSessionExpired.value = false
  router.push('/login')
  clearInterval(sessionInterval)
  addActivityListeners()
  sessionInterval = setInterval(checkGlobalSession, 1000)
}

const addActivityListeners = () => {
  window.addEventListener('mousemove', () => resetSessionTimer(false), { capture: true, passive: true })
  window.addEventListener('keydown', () => resetSessionTimer(true), { capture: true, passive: true })
  window.addEventListener('click', () => resetSessionTimer(true), { capture: true })
  window.addEventListener('scroll', () => resetSessionTimer(false), { capture: true, passive: true })
  window.addEventListener('touchstart', () => resetSessionTimer(false), { capture: true, passive: true })
}

const removeActivityListeners = () => {
  window.removeEventListener('mousemove', () => resetSessionTimer(false), { capture: true })
  window.removeEventListener('keydown', () => resetSessionTimer(true), { capture: true })
  window.removeEventListener('click', () => resetSessionTimer(true), { capture: true })
  window.removeEventListener('scroll', () => resetSessionTimer(false), { capture: true })
  window.removeEventListener('touchstart', () => resetSessionTimer(false), { capture: true })
}

onMounted(() => {
  localStorage.setItem('loginTime', Date.now().toString())
  lastSavedTime = Date.now()
  
  // Klasörlere basıldığında giden Axios isteklerini de dinle
  axios.interceptors.request.use((config) => {
    if (!config.url.includes('/api/session/log')) {
      resetSessionTimer(true)
    }
    return config
  }, (error) => { return Promise.reject(error) })

  checkGlobalSession()
  sessionInterval = setInterval(checkGlobalSession, 1000)
  addActivityListeners()
})

onUnmounted(() => {
  if (sessionInterval) clearInterval(sessionInterval)
  removeActivityListeners()
})
</script>