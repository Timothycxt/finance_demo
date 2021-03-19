<template>
   <div class="app-container">
      <el-alert :closable="false" title="公司列表"  type="success"/>
        <!--顶部查询栏-->
       <!--查询表单-->
    <el-form :inline="true" class="demo-form-inline" model="searchObj">
     <el-form-item style="width: 100px;">
        <el-input v-model="searchObj.code" placeholder="CODE"/>
      </el-form-item>
      <el-form-item style="width: 120px;">
        <el-input v-model="searchObj.name" placeholder="公司名"/>
      </el-form-item>
    <el-form-item style="width: 100px;">
        <el-input v-model="searchObj.legalPerson" placeholder="法人"/>
      </el-form-item>
        <el-form-item>
        <el-input v-model="searchObj.industry" placeholder="行业"/>
      </el-form-item> 
      <el-form-item label="创立时间">
        <el-date-picker
          v-model="searchObj.establishDate"
          type="datetime"
          placeholder="选择创立时间"
          value-format="yyyy-MM-dd HH:mm:ss"
          default-time="00:00:00"
        />
      </el-form-item>
      <el-button type="primary" icon="el-icon-search" @click="getCorpList()">查询</el-button>
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

      <el-table-column label="公司编码"   align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.code }}</span>
        </template>
      </el-table-column>

      <el-table-column label="公司名字"  align="center">
        <template slot-scope="scope">
          {{ scope.row.name}}
        </template>
      </el-table-column>

      <el-table-column label="法人" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.legalPerson}}
        </template>
      </el-table-column>

     <el-table-column label="领域" width="120" align="center">
        <template slot-scope="scope">
          {{ scope.row.industry}}
        </template>
      </el-table-column>
  
      <el-table-column align="center" prop="created_at" label="创立时间" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.establishDate }}</span>
        </template>
      </el-table-column>

      <el-table-column label="operation" width="200" align="center">
        <template slot-scope="scope">
          <router-link :to="'/corp/read/'+scope.row.id+'/'+scope.row.name">
            <el-button type="primary" size="mini" icon="el-icon-view">查看</el-button>
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
      @current-change="getCorpList"/>
  </div>

</template>

<script>
import {getCorpInfoPageList }from '@/api/corp'

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
        this.getCorpList()
        
    },
    //写具体的方法调用
    methods: {
        getCorpList (page = 1){// 调用api层获取数据库中的数据
            this.page = page
            getCorpInfoPageList(this.page,this.limit,this.searchObj)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            //每页数据
            this.list = response.data.items
            //总记录数
            this.total = response.data.total
            console.log(response.data.total)
            this.listLoading = false
            })
            .catch(response => { // 如果请求失败，执行catch里面操作

            })
        },

        resetData(){
            this.searchObj = {}
            this.getCorpList()
             }
    }
    
}
</script>