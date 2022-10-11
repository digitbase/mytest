<template>
  <el-container>
    <el-header>
      <div>
        <img src="../assets/logo.png" alt="logo" />
        <div><span>你好</span></div>
      </div>
      <div>
        <el-button>222</el-button>
      </div>
    </el-header>
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="this.collapse?64:200" ref="myBox">
        <div class="toggle-button" @click="toggleClick">|||</div>
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#333744"
          text-color="#fff"
          active-text-color="#409Bff"
          :unique-opened = true
          :collapse-transition = false
          :collapse= this.collapse
          
        >
          <!-- 一级菜单 -->
          <el-submenu :index="item.id" v-for="item in menulist" :key="item.id">
            <!-- 一级菜单横版 -->
            <template slot="title">
              <i class="iconfont" :class="item.icon"></i>
              <span>{{ item.name }}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item
              :index="subItem.id"
              v-for="subItem in item.children"
              :key="subItem.id"
            >
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span>{{ subItem.name }}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
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
export default {
  data() {
    return {
      collapse : false,
      menulist: [
        {
          id: 1,
          name: 'Menulist1',
          icon: 'icon-user',
          children: [
            { id: 1, name: 'sub1' },
            { id: 2, name: 'sub2' },
            { id: 3, name: 'sub3' },
          ],
        },
        {
          id: 2,
          name: 'Menulist2',
          icon: 'icon-add',
          children: [
            { id: 1, name: 'sub1' },
            { id: 2, name: 'sub2' },
            { id: 3, name: 'sub3' },
          ],
        },
        { id: 3, name: 'Menulist3', icon: 'icon-cart-full' },
      ],
    }
  },
  created() {
    this.getMenList()
  },
  methods: {

    toggleClick(){
      this.collapse = !this.collapse;

      console.log(this.$refs.myBox.width)
    },
    async getMenList() {
      const { data: res } = await this.$axios.get('/menus/web')
      console.log(res['/space'])
      //this.menulist = res
    },
  },
}
</script>

<style lang="scss" scoped>
.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  align-items: center;
  div {
    display: flex;
    align-items: center;
    span {
      margin-left: 10px;
      color: white;
    }
  }
}
.el-aside {
  background-color: #333744;
  .el-menu{
    box-sizing: border-box;
    border-right: none;
  }
}
.el-main {
  background-color: #333;
}
.el-container {
  height: 100%;
}

.iconfont {
  margin-right: 10px;
}
.toggle-button{
  background-color: #4A5064;
  color: #fff;
  font-size: 10px;
  line-height: 24px;
  align-items:center;
  letter-spacing: 0.2em;
  text-align: center;
  cursor: pointer;
}
</style>
