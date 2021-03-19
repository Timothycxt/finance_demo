import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: '知识图谱',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '知识图谱', icon: 'el-icon-orange' }
    }]
  },

  {
    path: '/corp',
    component: Layout,
    redirect: '/corp/list',
    name: '公司',
    meta: { title: '公司', icon: 'el-icon-office-building' },
    children: [
      {
        path: 'list',
        name: '公司列表',
        component: () => import('@/views/finance/corp/index'),
        meta: { title: '公司列表', icon: 'el-icon-office-building' }
      },
      {
        path: 'read/:id/:name',
        name: '查看公司',
        component: () => import('@/views/edu/teacher/form'),
        meta: { title: '查看公司', icon: 'table' },
        hidden:true
      }
    ]
  },

  {
    path: '/industy',
    component: Layout,
    redirect: '/industy/biologicalMedicine',
    name: '行业新闻',
    meta: {
      title: '行业新闻',
      icon: 'nested'
    },
    children: [
      {
        path: 'energyCar',
        // (id) => {}
        component: () => import('@/views/finance/indu/energyCar'),
        name: 'industry1',
        meta: { title: '新能源汽车' }
      },
      {
        path: 'biologicalMedicine',
        // (id) => {}
        component: () => import('@/views/finance/indu/index'),
        name: 'industry2',
        meta: { title: '生物医药' }
      }
    ]
  },
  {
    path: '/economic',
    component: Layout,
    children: [
      {
        path: 'news',
        name: '经济新闻',
        component: () => import('@/views/finance/economic/index'),
        meta: { title: '经济新闻', icon: 'form' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
