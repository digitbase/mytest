import Vue from 'vue'
//导入路由
import Router from 'vue-router'

import Test from '../views/testPage.vue'
import Login from '../components/Login.vue'
import Home from '../components/HomePage.vue'
import Index from '../components/IndexPage.vue'
import Welcome from '../components/Welcome.vue'
import Sub1 from '../components/user/Sub1.vue'
import Sub2 from '../components/user/Sub2.vue'
import Sub3 from '../components/user/Sub3.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'test', component: Login },
    {
      path: '/index',
      name: 'index',
      component: Index,
      redirect: '/welcome',
      children: [
        { path: '/welcome', component: Welcome },
        { path: '/sub1', component: Sub1 },
        { path: '/sub2', component: Sub2 },
        { path: '/sub3', component: Sub3 },
      ],
    },
  ],
})

// router.beforeEach()

export default router
