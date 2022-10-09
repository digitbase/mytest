<template>
	<div class="login_container">
		<div class="login_box">
			<div class="avatar_box">
				<img src="../assets/logo.png" alt="placehold" />
			</div>
			<div>
				<el-form class="login_form" label-width="0px">
					<el-form-item prop="name">
						<el-input prefix-icon="iconfont icon-user"></el-input>
					</el-form-item>

					<el-form-item prop="password">
						<el-input
							prefix-icon="iconfont icon-password"></el-input>
					</el-form-item>

					<el-form-item prop="button" class="btns">
						<el-button type="primary">登录</el-button>
						<el-button type="info">重置</el-button>
					</el-form-item>
				</el-form>
			</div>
		</div>
	</div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.login_container {
	background: #2b4b6b;
	height: 100%;
}
.login_box {
	width: 450px;
	height: 300px;
	background-color: #fff;
	border-radius: 3px;
	position: absolute;
	left: 50%;
	top: 50%;
	transform: translate(-50%, -50%);
}
.avatar_box {
	height: 130px;
	width: 130px;
	border-radius: 50%;
	border: 2px solid #eee;
	padding: 10px;
	position: absolute;
	left: 50%;
	top: 0%;
	background-color: #fff;
	box-align: 0 0 10px #ddd;
	transform: translate(-50%, -50%);
	img {
		width: 100%;
		height: 100%;
		border-radius: 50%;
		background-color: #eee;
	}
}
.login_form {
	position: absolute;
	bottom: 0px;
	width: 100%;
	padding: 0 20px;
	box-sizing: border-box;
	.btns {
		display: flex;
		justify-content: flex-end;
	}
}
</style>
