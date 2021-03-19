<template>
   <div class="app-container">
       教师页面
    <!--顶部查询栏-->
       <!--查询表单-->
    <el-form :inline="true" class="demo-form-inline" model="searchObj">
    <el-form-item label-width="50">
        <el-input v-model="searchObj.id" placeholder="讲师ID"/>
      </el-form-item>
      <el-form-item>
        <el-input v-model="searchObj.name" placeholder="讲师名"/>
      </el-form-item>
      <el-form-item style="width: 145px;">
        <el-select v-model="searchObj.level" clearable placeholder="讲师头衔">
          <el-option :value="1" label="高级讲师"/>
          <el-option :value="2" label="首席讲师"/>
        </el-select>
      </el-form-item>
      <el-form-item label="添加时间">
        <el-date-picker
          v-model="searchObj.begin"
          type="datetime"
          placeholder="选择开始时间"
          value-format="yyyy-MM-dd HH:mm:ss"
          default-time="00:00:00"
        />
      </el-form-item>
      <el-button type="primary" icon="el-icon-search" @click="getTeacherList()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

     <!--表单页面-->  
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>

      <el-table-column label="Introduce"  width="297" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.intro }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Name" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.name}}
        </template>
      </el-table-column>

  
      <el-table-column class-name="status-col" label="Level" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.level| statusFilter">{{ scope.row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Display_time" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.gmtCreate }}</span>
        </template>
      </el-table-column>

      <el-table-column label="operation" width="200" align="center">
        <template slot-scope="scope">
          <router-link :to="'/edu/teacher/edit/'+scope.row.id">
            <el-button type="primary" size="mini" icon="el-icon-edit">查看</el-button>
          </router-link>
          <el-button type="danger" size="mini" icon="el-icon-delete" @click="removeDataById(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

 <el-pagination
      :current-page="page"
      :page-size="limit"
      :total="total"
      style="padding: 30px 0; text-align: center;"
      layout="total, prev, pager, next, jumper"
      @current-change="getTeacherList"/>
  </div>

</template>

<script>
import Teacher from '@/api/teacher.js'

export default {
    filters: {
    statusFilter(status) {
      const statusMap = {
        1: 'success',
        2: 'gray',
        3: 'danger'
      }
      return statusMap[status]
    }
  },
    //定义变量和初始值
    data () {
      return{
          listLoading : true,
          list: null,// 数据列表
          total: 0,// 总记录数
          page: 1,// 页码
          limit: 10,// 每页记录数
          searchObj: {}// 条件封装对象
      }
    },
    //在页面渲染之前调用，调用具体某个方法
    created() {
        // 调用方法
        this.getTeacherList()
        
    },
    //写具体的方法调用
    methods: {
        getTeacherList (page = 1){// 调用api层获取数据库中的数据
            this.page = page
            Teacher.getTeacherPageList(this.page,this.limit,this.searchObj)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            //每页数据
            this.list = response.data.items
            //总记录数
            this.total = response.data.total
            //console.log(this.list)
            console.log(this.searchObj)
            this.listLoading = false
            })
            .catch(response => { // 如果请求失败，执行catch里面操作

            })
        },

        resetData(){
            this.searchObj = {}
            this.getTeacherList()
             }
    }
    
}
</script>