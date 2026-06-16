import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './assets/main.css'

// 🛡️ KÜRESEL GÜVENLİK BİLETİ TAŞIYICISI (AXIOS INTERCEPTOR)
// Bu kod, siteden backend'e giden her isteğin (dosya listeleme, indirme vs.) 
// başına otomatik olarak kullanıcının dijital giriş token'ını ekler.
axios.interceptors.request.use(
  (config) => {
    const userSession = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')
    if (userSession && userSession.token) {
      config.headers.Authorization = `Bearer ${userSession.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
);

// 🛡️ OTURUM SÜRESİ DOLDUĞUNDA OTOMATİK ÇIKIŞ YAPMA
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      // Eğer biletin süresi dolmuşsa veya geçersizse kullanıcıyı güvenli bir şekilde dışarı atar
      localStorage.removeItem('bonna_user_session')
      localStorage.removeItem('loginTime')
      router.push('/login')
    }
    return Promise.reject(error)
  }
);

const app = createApp(App)

app.use(router)

app.mount('#app')