import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from './router'

import Router from 'vue-router'
import Vuex from 'vuex'
import store from "@/vuex/store";


Vue.use(ElementUI);

Vue.use(router)
Vue.config.productionTip = false
// debugger;

Vue.prototype.$appName = 'My App'
// Vue.prototype._ = _;

console.log(router)

new Vue({
  router,
  el: '#app',
  router,
  data: {
 
  },
  computed: {

  },
  render: h => h(App),
})

