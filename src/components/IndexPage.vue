<template>
  <el-container>
    <el-header>
      <div>
        <img src="../assets/logo.png" alt="logo" />
        <div><span>你好</span></div>
      </div>
      <div>
        <el-button name="testBtn" v-on:click="btnClick($event)">222</el-button>
      </div>
    </el-header>
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="this.navWith" ref="myBox">
        <div class="toggle-button" @click="toggleClick">|||</div>
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#333744"
          text-color="#fff"
          active-text-color="#409Bff"
          :unique-opened="true"
          :collapse-transition="false"
          :collapse="this.collapse"
          :router="true"
          :default-active="this.activePath"
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
              :index="subItem.path"
              v-for="subItem in item.children"
              :key="subItem.id"
              @click="saveNavState(subItem.path, $event)"
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
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      navWith: '200px',
      collapse: false,
      activePath: '',
      menulist: [
        {
          id: 1,
          name: 'Menulist1',
          icon: 'icon-user',
          children: [
            { id: 1, name: 'sub1', path: '/sub1' },
            { id: 2, name: 'sub2', path: '/sub2' },
            { id: 3, name: 'sub3', path: '/sub3' },
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
    this.activePath = window.sessionStorage.getItem('activePath')
  },
  methods: {
    btnClick(event) {
      console.log(event.target) // 当前元素点击的子节点
      console.log(event.currentTarget) // 当前Vue元素

      var pro = event.currentTarget // 当前元素

      pro.lastElementChild.style.color = '#DE3E3E' // 修改最后一个子节点，改变图标和文字颜色

      console.log(pro.getAttribute('name')) // 获取html元素属性值
    },
    saveNavState(obj, e) {
      window.sessionStorage.setItem('activePath', obj)
      this.activePath = obj
    },
    toggleClick() {
      this.collapse = !this.collapse
      this.navWith = this.collapse ? '64px' : '200px'

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
  .el-menu {
    box-sizing: border-box;
    border-right: none;
  }
}
.el-main {
}
.el-container {
  height: 100%;
}

.iconfont {
  margin-right: 10px;
}
.toggle-button {
  background-color: #4a5064;
  color: #fff;
  font-size: 10px;
  line-height: 24px;
  align-items: center;
  letter-spacing: 0.2em;
  text-align: center;
  cursor: pointer;
}
</style>
