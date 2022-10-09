import Vue from "vue";
import App from "./App";

import router from "./router";


import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
Vue.use(ElementUI);

Vue.use(router);
Vue.config.productionTip = false;


Vue.prototype.$appName = "My App";


console.log(router);

new Vue({
	router,
	el: "#app",
	router,
	data: {},
	computed: {},
	render: (h) => h(App),
});
