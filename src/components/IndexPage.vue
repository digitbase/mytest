<template>
  <el-container>
    
   
      <el-header>
        <div>
          <img src="../assets/logo.png" alt="logo" />
          <div><span>你好</span></div>
        </div>
        <div>
          <el-button >222</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">Aside</el-aside>
      <el-main>
        <div class="container">
          <el-input
							prefix-icon="iconfont icon-password"
						
							type="password"
						></el-input>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {}
</script>

<style lang="scss" scoped>
.el-header{
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  align-items:center;
  div {
   display: flex; 
   align-items: center;
   span {
    margin-left: 10px;
    color: white;
   }
  }
}
.el-aside{
  background-color: #333744;
}
.el-main{
  background-color: #333;
}
.el-container{
  height: 100%;
}

</style>
