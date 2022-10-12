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
        <el-table :data="carList" style="width: 100%" border>
          <!-- 索引列 -->
          <el-table-column type="index" label="ID"> </el-table-column>
          <el-table-column prop="id" label="日期" width="120px">
          </el-table-column>
          <el-table-column prop="masterName" label="姓名"> </el-table-column>
          <el-table-column prop="groupName" label="状态"> </el-table-column>
          <el-table-column label="地址">
            <template slot-scope="scope">
              <el-switch
                v-model="scope.row.levelNum"
                @change="handleLevelNumChange(scope.row)"
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
            :page-sizes="[2, 4, 5]"
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
    //this.getInfo()
    this.getTest()
  },
  data() {
    return {
      userList: [],
      carList: [],
      queryInfo: {
        pageNum: 1,
        pageSize: 2,
        total: 0,
        start: 0,
      },
    }
  },
  methods: {
    //修改状态
    async handleLevelNumChange (info) {
      console.log(info)
      console.log(info.id)
      console.log(info.levelNum)


      let postData = {
        "id" : info.id,
        "levelNum" : 3
      }

      await this.$axios
        .post('/service/Inspection/0.1.0/InspectionCheckGroup/update', postData, {
          headers: {
            'Content-Type': 'application/json',
            Connection: 'keep-alive',
          },
        })
        .then((res) => {
          console.log(res)
          if (res.status == 201 || res.status == 200) {

            this.$message.success('更新成功')
          } else {
            this.$message.error('更新error')
          }
        })

    },

    // pageSize改变
    handleSizeChange(pageSize) {
      this.queryInfo.pageSize = pageSize
      this.queryInfo.start = 0
      this.getTest()
    },
    // 页码改变事件
    handleCurrentChange(pageNum) {
      this.queryInfo.start = this.queryInfo.pageSize * (pageNum -1)

      console.log(this.queryInfo)


      this.getTest()
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
    async getTest() {
      let sss = {
        start: this.queryInfo.start,
        limit: this.queryInfo.pageSize,
        condition: {},
        orderby: [{ field: 'groupName', order: 'desc' }],
      }

      console.log(sss)
      await this.$axios
        .post('/service/Inspection/0.1.0/InspectionCheckGroup/query', sss, {
          headers: {
            'Content-Type': 'application/json',
            Connection: 'keep-alive',
          },
        })
        .then((res) => {
          // console.log(res)
          if (res.status == 201 || res.status == 200) {
            this.carList = res.data.result[0].InspectionCheckGroup
            this.queryInfo.total = res.data.result[0].count * 1

            console.log(this.queryInfo)
            this.$message.success('car sub1')
          } else {
            this.$message.error('car error')
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
