import Vue from "vue";
import App from "./App";

import router from "./router";


import ElementUI from "element-ui";

import "element-ui/lib/theme-chalk/index.css";
import "./assets/fonts/iconfont.css";
import "./assets/css/global.scss";

Vue.use(ElementUI);

Vue.use(router);
Vue.config.productionTip = false;


Vue.prototype.$appName = "My App";


import axios from "axios";
axios.defaults.baseURL = "http://192.168.40.188:8000/"
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.post['Access-Control-Allow-Headers'] = "X-Requested-With,Content-Type"
window.$axios = Vue.prototype.$axios = axios;


console.log(router);

new Vue({
	router,
	el: "#app",
	router,
	data: {},
	computed: {},
	render: (h) => h(App),
});
