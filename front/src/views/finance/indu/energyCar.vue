<template>
  <div class="hello">
    <div id="app">
     <el-alert :closable="false" title="新能源汽车行业新闻词云图"  type="success"/>
      <wordcloud
      :data="defaultWords"
      nameKey="name"
      valueKey="value"
      :color="myColors"
      :showTooltip="false"
      :wordClick="wordClickHandler"
      drawOutOfBound:true>
      </wordcloud>
    </div>
<el-alert :closable="false" title="新能源汽车行业新闻列表"  type="success"/>
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

      <el-table-column label="Title"   align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Source"  align="center">
        <template slot-scope="scope">
          {{ scope.row.source}}
        </template>
      </el-table-column>

      <el-table-column label="Link" width="200" align="center">
        <template slot-scope="scope">
       <el-link :href= scope.row.link target="_blank">{{scope.row.link}}</el-link>
        </template>
      </el-table-column>

     <el-table-column label="industry" width="100" align="center">
        <template slot-scope="scope">
          {{ scope.row.industy}}
        </template>
      </el-table-column>
  
      <el-table-column align="center" prop="created_at" label="Publish Date" width="150">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.publishDate }}</span>
        </template>
      </el-table-column>

      <el-table-column label="operation" width="200" align="center">
        <template slot-scope="scope">
          <router-link :to="'/corp/read/'+scope.row.id+'/'+scope.row.name">
            <el-button type="primary" size="mini" icon="el-icon-view">查看</el-button>
          </router-link>
        </template>
      </el-table-column>
    </el-table>

 <el-pagination
      :current-page="page"
      :page-size="limit"
      :total="total"
      style="padding: 30px 0; text-align: center;"
      layout="total, prev, pager, next, jumper"
      @current-change="getInduList"/>

  </div>
</template>

<script>
import {getInduPageList} from '@/api/corp.js'
import {getWordsCloud} from '@/api/corp.js'
import wordcloud from 'vue-wordcloud'
import { formatTime } from '@/utils'
export default {
  name: 'WordCloud',
  components: {
    wordcloud
  },
  methods: {
    wordClickHandler (name, value, vm) {
      console.log('wordClickHandler', name, value, vm)
    },
    getWordsCloudList(industry){
        console.log("进入wordsCloudList函数" + industry)
      getWordsCloud(industry)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            console.log("success")
            this.defaultWords = response.data.defaultWords
            })
            .catch(response => { // 如果请求失败，执行catch里面操作
            console.log("error555")
            })
    },
    getInduList(page = 1){
          console.log("进入getInduList函数" + this.induName)
          this.page = page
      getInduPageList(this.page,this.limit,this.induName,this.searchObj)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            console.log("success")
            this.listLoading = false
            this.total = response.data.total
            this.list = response.data.items
            })
            .catch(response => { // 如果请求失败，执行catch里面操作
            console.log("error666")
            })
    }
  },
  data () {
    return {
        listLoading : true,
        induName :'',
        list: null,// 数据列表
        total: 0,// 总记录数
        page: 1,// 页码
        limit: 6,// 每页记录数
        searchObj: {},// 条件封装对象
        myColors: ['#1f77b4', '#629fc9', '#94bedb', '#c9e0ef'],
        defaultWords: [ ],
    }
  },
  created(){
    const industry = '新能源汽车'
    this.induName = industry
    this.getWordsCloudList(industry)
    this.getInduList()
  }
}
</script>
