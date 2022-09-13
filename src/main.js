import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

import router from './router'
import Router from 'vue-router'
Vue.use(Router)

Vue.config.productionTip = false
debugger;

new Vue({
  el: '#app',
  data: {
    currentRoute: window.location.pathname
  },
  computed: {

  },
  render: h => h(App),
})