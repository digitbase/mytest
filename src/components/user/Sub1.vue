<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>活动管理</el-breadcrumb-item>
      <el-breadcrumb-item>活动列表</el-breadcrumb-item>
      <el-breadcrumb-item>活动详情</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            placeholder="请输入内容"
            v-model="input3"
            class="input-with-select"
          >
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary">添加用户</el-button>
        </el-col>
      </el-row>

      <el-row>
        <el-table :data="userList" style="width: 100%" border>
          <!-- 索引列 -->
          <el-table-column type="index" label="ID"> </el-table-column>
          <el-table-column prop="id" label="日期" width="120px">
          </el-table-column>
          <el-table-column prop="name" label="姓名"> </el-table-column>
          <el-table-column prop="member_num" label="状态"> </el-table-column>
          <el-table-column label="地址">
            <template slot-scope="scope">
              <el-switch
                v-model="scope.row.is_output_counted"
                active-color="#13ce66"
                inactive-color="#ff4949"
              >
              </el-switch>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180px">
            <template slot-scope="scope">
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
              ></el-button>
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
              ></el-button>
              <el-tooltip
                class="item"
                effect="dark"
                content="编辑文字"
                placement="top"
                :enterable="false"
              >
                <el-button
                  type="warning"
                  icon="el-icon-setting"
                  size="mini"
                ></el-button>
              </el-tooltip>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
      <el-row class="page_row">
        <div class="block">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryInfo.pageNum"
            :page-sizes="[10, 20, 30, 40]"
            :page-size="queryInfo.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="queryInfo.total"
          >
          </el-pagination>
        </div>
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  created() {
    this.getInfo()
  },
  data() {
    return {
      userList: [],
      queryInfo:{
        pageNum:1,
        pageSize:20,
        total:0,
      }
    }
  },
  methods: {
    // pageSize改变
    handleSizeChange(pageSize){

    },
    // 页码改变事件
    handleCurrentChange(pageNum){

    },
    async getInfo() {
      await this.$axios
        .get('/api/spaces', { params: { key: 'value' } })
        .then((res) => {
          if (res.status == 200) {
            this.userList = res.data
            this.$message.success('sub1')
          } else {
            this.$message.error('sub1 error')
          }
        })
    },
  },
}
</script>

<style lang="scss" scoped>
.el-breadcrumb {
  margin-bottom: 15px;
}
.el-card {
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15) !important;
}
.el-table {
  margin-top: 20px;
}
.page_row {
  margin-top: 20px;
  text-align: right;
}
</style>
