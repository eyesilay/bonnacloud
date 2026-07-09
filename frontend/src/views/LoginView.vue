<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 font-sans p-4 relative select-none">
    
    <div class="absolute top-4 right-4 flex items-center border border-slate-200 rounded-xl px-2 py-1.5 bg-white text-xs font-bold shadow-sm z-50">
      <select :value="currentLang" @change="setLanguage($event.target.value)" class="bg-transparent border-none outline-none cursor-pointer pr-1 text-slate-800 font-bold focus:ring-0 text-xs">
        <option value="tr">TR</option>
        <option value="en">EN</option>
      </select>
    </div>

    <div class="max-w-md w-full bg-white rounded-3xl shadow-xl p-8 border border-slate-100 relative">
      <div class="flex flex-col items-center justify-center mb-6 text-center">
        <img src="https://bonna-website.b-cdn.net/bonnacloud-assets/BonnaCloud-Logo.png" alt="Bonna Cloud" class="h-14 w-auto object-contain mb-4" />
        <h2 class="text-base font-black text-slate-900 tracking-tight">{{ t.loginTitle }}</h2>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-5">
        <div v-if="errorMessage" class="bg-red-50 text-red-600 text-sm font-bold p-4 rounded-xl border border-red-100 text-center animate-fade-in">
          {{ errorMessage }}
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-2">{{ t.emailAddress }}</label>
          <input v-model="email" type="email" required placeholder="name@company.com" class="w-full bg-slate-50 border border-slate-200 text-sm font-medium text-slate-900 placeholder-slate-400 px-4 py-3.5 rounded-xl focus:outline-none focus:border-theme-primary focus:ring-1 focus:ring-theme-primary transition-all" />
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-2">{{ t.passwordLabel }}</label>
          <input v-model="password" type="password" required placeholder="••••••••" class="w-full bg-slate-50 border border-slate-200 text-sm font-medium text-slate-900 placeholder-slate-400 px-4 py-3.5 rounded-xl focus:outline-none focus:border-theme-primary focus:ring-1 focus:ring-theme-primary transition-all" />
        </div>

        <button type="submit" :disabled="isLoading" class="w-full py-4 bg-theme-primary text-slate-900 font-black rounded-xl hover:bg-yellow-500 transition-all shadow-md active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-50 mt-4">
          <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
          </svg>
          {{ isLoading ? t.authenticating : t.signIn }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { currentLang, setLanguage, t } from '../utils/i18n.js'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true
  try {
    const response = await axios.post(`${window.location.origin}/api/login`, {
      email: email.value.trim(),
      password: password.value
    })
    
    localStorage.setItem('bonna_user_session', JSON.stringify(response.data))
    localStorage.setItem('loginTime', Date.now().toString())
    router.push('/dashboard')
  } catch (e) {
    if (e.response) {
      if (e.response.status === 401 || e.response.status === 403) {
         errorMessage.value = t.value.loginInvalidCredentials
      } else {
         errorMessage.value = `${t.value.loginSystemError} (${e.response.status}): ${e.response.data.detail || t.value.loginDatabaseError}`
      }
    } else {
      errorMessage.value = t.value.loginServerConnectionError
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>