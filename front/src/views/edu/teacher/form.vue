<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20" style="height:825px;">
                    <div class="user-info">
                            <div class="user-info-name">{{ corpInfo.name }}</div>
                    </div>
                    <div class="user-info-list">
                        公司编码：
                        <span>{{corpInfo.code}}</span>
                    </div>
                    <div class="user-info-list">
                        创立时间：
                        <span>{{corpInfo.establishDate}}</span>
                    </div>
                    <div class="user-info-list">
                        公司法人：
                        <span>{{corpInfo.legalPerson}}</span>
                    </div>
                    <div class="user-info-list">
                        注册资本：
                        <span>{{corpInfo.registCapital}}</span>
                    </div>
                    <div class="user-info-list">
                        注册地点：
                        <span>{{corpInfo.adminDiv}}</span>
                    </div>

<el-collapse :value="opened" v-model="activeName" @change="handleChange">

  <el-collapse-item title="业务范围" name="1">
                    <div class="user-info-list">
                        <div>{{corpInfo.businessScope}}</div>
                    </div>
  </el-collapse-item>
   <el-collapse-item title="组成成员" name="1">
                    <div class="user-info-list">
                        <div>{{corpInfo.member}}</div>
                    </div>
  </el-collapse-item>
     <el-collapse-item title="所属行业" name="1">
                    <div class="user-info-list">
                        <div>{{corpInfo.industry}}</div>
                    </div>
  </el-collapse-item>

</el-collapse>
                </el-card>
                <el-card shadow="hover" style="height:156px;">
                    <div slot="header" class="clearfix">
                        <span>公司新闻情感分析结果</span>
                    </div>
                     <el-row :gutter="20" class="mgb20" style = "padding-top:0">
                      <el-col :span="8">
                            <div class="grid-content grid-con-1">
                                <div class="grid-cont-right">
                                    <div>正面新闻数量</div>
                                    <div class="grid-num">{{emotion.positive}}</div>
                                </div>
                            </div>
                    </el-col>
                    <el-col :span="8">
                            <div class="grid-content grid-con-2">
                                <div class="grid-cont-right">
                                    <div>中等新闻数量</div>
                                    <div class="grid-num">{{emotion.middle}}</div>
                                </div>
                            </div>
                    </el-col>
                    <el-col :span="8">
                            <div class="grid-content grid-con-3">
                                <div class="grid-cont-right">
                                    <div>负面新闻数量</div>
                                    <div class="grid-num">{{emotion.negative}}</div>
                                </div>
                            </div>
                    </el-col>
                </el-row>
                </el-card>
            </el-col>
            <el-col :span="16">
                 <!-- 这里的标签名称要和main.js文件中定义的组件名称保持一致 -->
                <el-card shadow="hover" style="height:1000px;">
                    <div slot="header" class="clearfix">
                        <span>公司相关新闻</span>
                    </div>
                <happy-scroll color="rgba(0,0,0,0.5)" size="5" style="width: 674px; height: 100%;" resize>
                  <div class="happy-scroll-container">
                    <el-table :show-header="false" 
                          v-loading="listLoading" 
                          element-loading-text="Loading"
                          fit
                          highlight-current-row
                          :data="list" 
                           style="width: 645px;">

                        <el-table-column  width="58">
                            <template slot-scope="scope">
                                <div class="news-date">
                                    <div>
                                {{scope.row.publish_date}}
                                    </div>
                                </div>
                            </template> 
                        </el-table-column>
                        <el-table-column>
                            <template slot-scope="scope">
                                <div class="news-title">
                                    <div>
                                        {{scope.row.title}}
                                        <el-tag :type="scope.row.emotion| statusFilter">
                                            {{ scope.row.emotion === 1?'发展向好':scope.row.emotion === 0?'平稳发展':'存有风险'}}
                                            </el-tag>
                                    </div>
                                </div>
                                <div class="news-keywords">
                                 <div>
                                    Abstract:{{scope.row.keywords}}
                                <el-link :href= scope.row.link target="_blank">{{scope.row.link}}</el-link>
                                 </div>
                                </div>                           
                                 </template>
                        </el-table-column>
                        <el-table-column width="55">
                            <template>
                                <i class="el-icon-view"></i>
                                <i class="el-icon-delete"></i>
                            </template>
                        </el-table-column>
                    </el-table>
                  </div>

            <el-pagination
      :current-page="page"
      :page-size="limit"
      :total="total"
      style="padding: 30px 0; text-align: center;"
      layout="total, prev, pager, next, jumper"
      @current-change="getCorpNews"/>
                      </happy-scroll>

                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="20">
                <el-col :span="24">
                     <el-card shadow="hover">
                       <schart ref="line" class="schart" canvasId="line" :options="options2"></schart>
                     </el-card>
                </el-col>
        </el-row>
    </div>
</template>

<script>
import Schart from 'vue-schart';
import bus from '@/components/common/bus';
import {getCorpInfoId} from '@/api/corp'
import {getCorpNewsPageList} from '@/api/corp'
import{getCorpNewsEmotionCount} from '@/api/corp'
import{getCorpScore} from '@/api/corp'
  import { formatTime } from '@/utils';

export default {
    name: 'dashboard',

    filters: {
    statusFilter(status) {
      const statusMap = {
        '1': 'success',
        '0': 'gray',
        '-1':'danger'
      }
      return statusMap[status]
    }
  },

    data() {

        return {
            activeName: '1',//展开name为1的折叠板
            listLoading : true,
            total : 0,
            page: 1,// 页码
            limit:7,// 每页记录数
            list:null,
            corpName:'',
            emotion:{
                postive : '0',
                negative: '0',
                middle: '0'
            },
            corpInfo:{
                 code:'',
                 name:'',
                 legalPerson:'',
                 registCapital:'',
                 industry:'',
                 type:'',
                 adminDiv:'',
                 establishDate:'',
                 businessScope:'',
                 member:''
            },
            options2: {
                type: 'line',
                title: {
                    text: '风险评估得分趋势图'
                },
                labels: ['1月','2月','3月','4月','5月','6月', '7月', '8月', '9月', '10月','11月','12月'],
                datasets: null
                
            },
            searchObj:{}
        };
    },
    components: {
        Schart
    },
    computed: {
        role() {
            return this.name === 'admin' ? '超级管理员' : '普通用户';
        }
    },
    created() {
    if (this.$route.params && this.$route.params.id && this.$route.params.name) {
       const id = this.$route.params.id
       const name = this.$route.params.name
       this.corpName = name
       console.log("created:"+this.corpName)
       console.log(id + " " + name)
       this.getCorpInfo(id)
        // 调用该公司新闻消息
       this.getCorpNews()
       // 调用该公司情感分析数据
       this.getCorpNewsEmotion()
       this.getCorpAllScore(id)
        }    
     },
    // },
    methods: {
        getCorpInfo(id){// 调用api层获取数据库中的数据
            getCorpInfoId(id).then(response => {// 如果请求成功，返回状态码20000，执行then里面操作
                this.corpInfo = response.data.corpInfo
                 this.listLoading = false
            }).catch(response => { // 如果请求失败，执行catch里面操作
            console.log("error")
            })
        },
        getCorpNews(page = 1){
            console.log("进入getCorpNewsList函数")
             name = this.corpName
             this.page = page
             console.log(page)
             console.log("输出corpInfo.name" + name)
            getCorpNewsPageList(this.page,this.limit,name,this.searchObj)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            //每页数据
            this.list = response.data.items
            console.log(this.list)
            //总记录数
            this.total = response.data.total
            console.log(response.data.total)
            this.listLoading = false
            })
            .catch(response => { // 如果请求失败，执行catch里面操作
            console.log("error22222")
            })
        },
        getCorpNewsEmotion(){
            console.log("进入getCorpNewsEmotion函数")
             name = this.corpName
             console.log("输出corpInfo.name" + name)
            getCorpNewsEmotionCount(name)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            //每页数据
            this.emotion = response.data.emotion
            })
            .catch(response => { // 如果请求失败，执行catch里面操作
            console.log("error3333")
            })
        },
        getCorpAllScore(id){
             console.log("进入etCorpAllScore函数")
            getCorpScore(id)
            .then(response => { // 如果请求成功，返回状态码20000，执行then里面操作
            this.options2.datasets = response.data.datasets
             console.log("success444")
            })
            .catch(response => { // 如果请求失败，执行catch里面操作
            console.log("error4444")
            })
        },
        changeDate() {
            const now = new Date().getTime();
            this.data.forEach((item, index) => {
                const date = new Date(now - (6 - index) * 86400000);
                item.name = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;
            });
        }
    }
};
</script>

<style scoped>
.el-row {
    margin-bottom: 20px;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}
.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}
.grid-num {
    font-size: 15px;
    font-weight: bold;
}
.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}
.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}
.grid-con-1 .grid-num {
    color: rgb(100, 213, 114);
}
.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}
.grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}

.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}

.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list div{
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.news-keywords div{
    font-size: 14px;
    color: #999;
    line-height: 25px;
}
.news-title div{
    font-size: 16px;
    color: rgb(247, 143, 7);
    border: #222;
    line-height: 25px;
}
.news-date div{
    color: rgb(7, 139, 247);
}
.mgb20 {
    margin-bottom: 20px;
}

.todo-item {
    font-size: 14px;
}

.todo-item-del {
    text-decoration: line-through;
    color: #999;
}

.schart {
    width: 100%;
    height: 300px;
}

.happy-sroll .happy-scroll-container {
width: 674px; height: 100%
}
</style>
