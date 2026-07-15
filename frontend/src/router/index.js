import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true } 
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true } 
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true } 
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

router.beforeEach((to, from, next) => {
  const userSession = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')

  if (to.meta.requiresAuth && !userSession) {
    return next('/login')
  }

  // 🌟 GÜNCELLEME: Admin paneline geçişte artık "superadmin" rolü de yetkili kabul ediliyor
  if (to.meta.requiresAdmin && (!userSession || (userSession.role !== 'admin' && userSession.role !== 'superadmin'))) {
    return next('/dashboard')
  }

  if (to.meta.guest && userSession) {
    return next('/dashboard')
  }

  next()
})

export default router