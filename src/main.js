import Vue from 'vue'
import App from './App'

import router from './router'

import ElementUI from 'element-ui'
import {Message} from "element-ui";

import 'element-ui/lib/theme-chalk/index.css'
import './assets/fonts/iconfont.css'
import './assets/css/global.scss'

Vue.use(ElementUI)

Vue.use(router)
Vue.config.productionTip = false

Vue.prototype.$appName = 'My App'
Vue.prototype.$message = Message;

import axios from 'axios'
axios.defaults.baseURL = "/api"
axios.interceptors.request.use(
  (config) => {
    config.headers.common['User-UUID'] = 'dcdb67d1-6116-4987-916f-6fc6cf2bc0e4'
    config.headers.common['token'] = 'a45619647715e4715ea0eebf45df6edabc0037db86cda4572d4569f78bfe4a118baeca07199b7f67e05f257a4ee3fdc5037bdf0d0e293622465d947290a0570a'
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

window.$axios = Vue.prototype.$axios = axios

console.log(router)

new Vue({
  router,
  el: '#app',
  router,
  data: {},
  computed: {},
  render: (h) => h(App),
})
