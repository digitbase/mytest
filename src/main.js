import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from './router'
import Router from 'vue-router'
import Vuex from 'vuex'
import store from "@/vuex/store";


Vue.use(ElementUI);



Vue.use(ElementUI);

Vue.config.productionTip = false
// debugger;

Vue.prototype.$appName = 'My App'
// Vue.prototype._ = _;


new Vue({
  router,
  el: '#app',
  data: {
    currentRoute: window.location.pathname
  },
  computed: {

  },
  render: h => h(App),
})

