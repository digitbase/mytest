import Vue from "vue";
//导入路由
import Router from "vue-router";
import Home from "../views/loginPage.vue";
import Test from "../views/testPage.vue";
import Login from "../components/Login.vue"


Vue.use(Router);

export default new Router({
	routes: [
		{ path: "/", redirect : "/login" },
		{ path: "/test", name: "test", component: Test },
    { path: "/login", name: "test", component: Login },
	],
});
