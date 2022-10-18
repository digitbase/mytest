<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>活动管理</el-breadcrumb-item>
      <el-breadcrumb-item>活动列表</el-breadcrumb-item>
      <el-breadcrumb-item>活动详情</el-breadcrumb-item>
    </el-breadcrumb>

    <el-row>
      <el-table
        :data="pageSpaceList"
        style="width: 100%"
        default-expand-all
        border
      >
        <!-- 索引列 -->
        <el-table-column type="expand" label="expand">
          <template slot-scope="scope">
            <el-col :span="2" style="background-color='#13ce66'"
              >&nbsp;8</el-col
            >
            <el-col :span="10" style="text-align: center">
              <el-row v-for="(o, i) in pageSpaceList" :key="o.id">
                <el-button size="small" type="success" :class="['rowbtn']"
                  >{{ o.name }}{{ i
                  }}<i class="el-icon-upload el-icon--right"></i
                ></el-button>
                <i class="el-icon-caret-right"></i>
              </el-row>
            </el-col>
            <!-- <pre>
                {{scope.row}}
                {{scope.row.cost_center.name}}
              </pre> -->
          </template>
        </el-table-column>
        <el-table-column type="index" label="ID"> </el-table-column>
        <el-table-column prop="id" label="日期" width="120px">
        </el-table-column>
        <el-table-column prop="name" label="name"> </el-table-column>
        <el-table-column prop="area" label="area"> </el-table-column>
        <el-table-column prop="timezone" label="timezone">
          <template slot-scope="scope">
            <!-- {{scope.row}} -->
          </template>
        </el-table-column>
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
              @click="editFormOpen(scope.row)"
            ></el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="mini"
              @click="showRoleDialog(scope.row)"
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
                @click="showRoleDialog(scope.row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-row>

    <!-- 添加用户对话框 -->
    <el-dialog
      title="添加用户"
      :visible.sync="dialogVisible"
      width="30%"
      @close="addFormClose"
      
    >
      <el-tree :data="this.state.data" :options="this.state.options" :isShowCheckbox="this.checkTree" ></el-tree>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addFormClick">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pageSpaceList: [],
      dialogVisible: true,
      checkTree:true,
      state: {
        data: [
          {
            id: 1,
            label: '一级 1',
            children: [
              {
                id: 4,
                label: '二级 1-1',
                children: [
                  {
                    id: 9,
                    label: '三级 1-1-1',
                  },
                  {
                    id: 10,
                    label: '三级 1-1-2',
                  },
                ],
              },
            ],
          },
          {
            id: 2,
            label: '一级 2',
            children: [
              {
                id: 5,
                label: '二级 2-1',
              },
              {
                id: 6,
                label: '二级 2-2',
              },
            ],
          },
          {
            id: 3,
            label: '一级 3',
            children: [
              {
                id: 7,
                label: '二级 3-1',
              },
              {
                id: 8,
                label: '二级 3-2',
              },
            ],
          },
        ],
        options: {
          children: 'children',
          label: 'label',
        },
      },
    }
  },
  created() {
    window.vuethis = this
    this.getPageSpaceList2()
  },
  methods: {
    editFormOpen(info) {
      console.log(info)
    },
    showRoleDialog(info) {
      console.log('click')
      this.dialogVisible = !this.dialogVisible
    },
    addFormClose() {},
    async getPageSpaceList() {
      await this.$axios
        .get('/api/tlapi/space', null, {
          headers: {
            'Content-Type': 'application/json',
            Connection: 'keep-alive',
          },
        })
        .then((res) => {
          console.log(res)

          if (res.status == 200) {
            if (res.data.resCode == 0) this.pageSpaceList = res.data.result
          } else {
            this.$message.error('car error')
          }
        })
    },

    async getPageSpaceList2() {
      let postDate = {
        condition: {},
        start: 0,
        limit: 20,
      }
      await this.$axios
        .post('/service/Permission/0.1.0/Permission/query', postDate, {
          headers: {
            'Content-Type': 'application/json',
            Connection: 'keep-alive',
          },
        })
        .then((res) => {
          if (res.status == 201 || res.status == 200) {
            this.pageSpaceList = res.data.result[0].permissions

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
.box-card {
  margin-top: 20px;
}
.rowbtn {
  margin: 10px 0;
}
</style>
