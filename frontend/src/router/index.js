import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true } // Sadece giriş yapmamış kişiler görebilir
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true } // Giriş yapmak zorunludur
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true } // Giriş yapmak ve Admin olmak zorunludur
    },
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard'
    }
  ]
})

// KİLİT VE OTOMATİK ÇIKIŞ MEKANİZMASI (ROUTE GUARD)
router.beforeEach((to, from, next) => {
  // Giriş bilgilerini ve giriş zamanını tarayıcı hafızasından çekiyoruz
  const userSession = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')
  const loginTime = localStorage.getItem('loginTime')

  // ⏱️ ÖN YÜZ OTOMATİK LOGOUT DENETİMİ
  // Arka uçtaki 180 dakikalık (3 saat) süre sınırını burada kontrol ediyoruz.
  if (userSession && loginTime) {
    const timePassed = Date.now() - parseInt(loginTime)
    const expireLimit = 1 * 60 * 1000 // 180 dakika milisaniye cinsinden (3 Saat)

    if (timePassed > expireLimit) {
      // 3 saat dolduysa oturum verilerini temizle ve login sayfasına fırlat
      localStorage.removeItem('bonna_user_session')
      localStorage.removeItem('loginTime')
      return next('/login')
    }
  }

  // Durum 1: Sayfa giriş gerektiriyor ama kullanıcı giriş yapmamış
  if (to.meta.requiresAuth && !userSession) {
    return next('/login')
  }

  // Durum 2: Sayfa sadece Admin yetkisi istiyor ama kullanıcının rolü admin değil
  if (to.meta.requiresAdmin && (!userSession || userSession.role !== 'admin')) {
    return next('/dashboard')
  }

  // Durum 3: Kullanıcı zaten giriş yapmış ama tekrar /login sayfasına gitmeye çalışıyor
  if (to.meta.guest && userSession) {
    return next('/dashboard')
  }

  // Her şey yolundaysa kullanıcının gitmek istediği sayfayı aç
  next()
})

export default router