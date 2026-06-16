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

// 🛡️ KİLİT MEKANİZMASI (ROUTE GUARD)
router.beforeEach((to, from, next) => {
  // Giriş bilgisini tarayıcı hafızasından çekiyoruz
  const userSession = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')

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