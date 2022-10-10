import Vue from 'vue'
//导入路由
import Router from 'vue-router'

import Test from '../views/testPage.vue'
import Login from '../components/Login.vue'
import Home from '../components/HomePage.vue'
import Index from '../components/IndexPage.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/test', name: 'test', component: Test },
    { path: '/login', name: 'test', component: Login },
    { path: '/home', name: 'home', component: Home },
    { path: '/index', name: 'index', component: Index },
  ],
})

// router.beforeEach()

export default router
