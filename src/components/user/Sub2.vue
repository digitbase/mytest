<template>
  <el-row>
    <el-table :data="queryList" style="width: 100%" border>
      <!-- 索引列 -->
      <el-table-column type="index" label="ID"> </el-table-column>
      <el-table-column prop="id" label="日期" width="200px"> </el-table-column>
      <el-table-column prop="routeName" label="routeName"></el-table-column>
      <el-table-column  label="status">
        <template slot-scope="scope">
          <el-tag type="success" v-if="scope.row.status=='active'">可用</el-tag>
          <el-tag type="warning" v-else>不可用</el-tag>
        </template>
        
      </el-table-column>
      <el-table-column  label="status">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="active"
            @change="handleActiveChange(scope.row)"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </template>
        
      </el-table-column>

     <!-- <el-table-column label="status">
        <template slot-scope="scope">
          <p>{{scope.row.status}}</p>
          <el-tag type="success" v-if="scope.row.status='active'">可用</el-tag>
          <el-tag type="warning" v-else-if="scope.row.status='deleted'">不可用</el-tag>
        </template>
      </el-table-column> -->
      <!--  <el-table-column label="地址">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="active"
            @change="handleActiveChange(scope.row)"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </template>
      </el-table-column> -->
      <el-table-column label="操作" width="180px">
        <template slot-scope="scope">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="editFormOpen(scope.row)"
          ></el-button>
          <el-button
            type="danger"
            icon="el-icon-delete"
            size="mini"
            @click="delFormOpen(scope.row)"
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
</template>

<script>
export default {
  created() {
    this.initTable()
  },
  data() {
    return {
      class_1: 'box',
      classArr: ['', 'box_green', ''],
      classObj: {
        box_black: false,
        box_red: true,
      },
      queryList: [],
    }
  },
  methods: {
    doThis: function () {
      alert('noclick')
    },
    dodo: function () {
      alert('dodo')
    },

    // 修改状态
    async handleActiveChange(info) {
      console.log(info.id)
      console.log(info.status)

      let status = info.status == 'active' ? 'active' : 'deleted'

      let postData = {
        id: info.id,
        status: status,
      }
      await this.$axios
        .post('service/Inspection/0.1.0/InspectionRoute/update', postData, {
          headers: {
            'Content-Type': 'application/json',
            Connection: 'keep-alive',
          },
        })
        .then((res) => {
          console.log(res)
          if (res.status == 201 || res.status == 200) {
            this.$message.success('更新成功')
            this.initTable()
          } else {
            this.$message.error('更新error')
          }
        })
    },

    //初始页面列表
    async initTable() {
      console.log('initTable')
      let postData = {
        start: 0,
        limit: 10,
        condition: {},
      }
      await this.$axios
        .post('/service/Inspection/0.1.0/InspectionRoute/query', postData, {
          headers: {
            'Content-Type': 'application/json',
            Connection: 'keep-alive',
          },
        })
        .then((res) => {
          console.log(res)
          if (res.status == 201 || res.status == 200) {
            // this.$message.success('接口成功')
            this.queryList = res.data.result[0].InspectionRoute
          } else {
            this.$message.error('更新error')
          }
        })
    },
  },
}
</script>

<style lang="scss" scoped></style>
