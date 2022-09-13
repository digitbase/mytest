<template>
	<div id="app">
		<img alt="Vue logo" src="./assets/logo.png" />
		<HelloWorld msg="Welcome to Your Vue.js App" />
		<el-button v-on:click="getData">{{ name }}</el-button>
		<el-button v-on:click="reversedMessage">{{ age }}</el-button>
		<p>Reversed message: "{{ name }}"</p>
		<p>Reversed message: "{{ now }}"</p>
		<p>姓:<el-input v-model="xing"></el-input></p>
		<p>名:<el-input v-model="ming"></el-input></p>
		<p v-show="ok">22222222222222</p>
		<p>{{ fullName }}</p>

		<el-table class="table" border :data="items" highlight-current-row>
			<el-table-column prop="id" label="ID" width="180"></el-table-column>
			<el-table-column
				prop="masterName"
				label="masterName"
				width=""
			></el-table-column>
			<el-table-column
				prop="createdDate"
				label="createdDate"
				width=""
			></el-table-column>
		</el-table>
		<ul>
			<li v-for="item in items" :key="item.id">
				{{ item.id }} - {{ item.masterName }}
			</li>
		</ul>
	</div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import axios from "axios";

export default {
	name: "App",
	components: {
		HelloWorld,
	},
	created() {
		let that = this;
		console.log("this is object");
		let data = {
			start: 0,
			limit: 10,
			condition: {},
		};
		axios
			.get(
				"http://192.168.31.186:3004/service/Inspection/0.1.0/InspectionCheckGroup/GetTree",
				data,
				{
					headers: {
						"Content-Type": "application/json",
						"Access-Control-Allow-Origin": "*",
						"Access-Control-Allow-Credentials": "true",
					},
				}
			)
			.then((res) => {
				console.log(res.resCode);
				if (res.status == 200) {
					let data = res.data;
					that.items = data.result[0].InspectionCheckGroup;
					for (let i of data.result[0].InspectionCheckGroup) {
						console.log(i);
					}
				}
			})
			.catch((err) => {
				console.log(err);
			});

		if (this.items.length < 1) {
			this.items = [
				{
					id: "as2dfasdf",
					groupName: "2",
					masterName: "",
					parentId: "",
					levelNum: 0,
					levelId: null,
					typeId: "PrimaryId",
					groupFlg: 2,
					customid: "customid",
					status: "deleted",
					createdBy: null,
					createdDate: "2022-08-30T02:59:26.000Z",
					lastModifiedBy: null,
					lastModifiedDate: "2022-08-30T02:59:26.000Z",
					owner: null,
				},
				{
					id: "adfasf2",
					groupName: "1",
					masterName: "",
					parentId: null,
					levelNum: 0,
					levelId: null,
					typeId: "PrimaryId",
					groupFlg: 2,
					customid: "customid",
					status: "active",
					createdBy: null,
					createdDate: "2022-08-30T06:57:46.000Z",
					lastModifiedBy: null,
					lastModifiedDate: "2022-08-30T06:57:46.000Z",
					owner: null,
				},
			];
		}
	},

	data() {
		return {
			name: "ihao",
			age: "ttt",
			xing: "佢",
			ming: "明",
			ok: false,
			items: [],
		};
	},
	methods: {
		getData() {
			if (this.name == "123") {
				this.name = "321";
				this.ok = false;
			} else {
				this.name = "123";
				this.ok = true;
			}
		},
		reversedMessage() {
			this.name.split("").reverse().join("");
		},
	},
	computed: {
		now: function () {
			return Date.now();
		},
		fullName() {
			console.log(this.items);
			return this.xing + this.ming;
		},
	},
	watch: {
		name(val) {
			this.nme = val + "111";
		},
	},
};
</script>

<style>
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
</style>
