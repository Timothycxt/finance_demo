import request from '@/utils/request'

    // 分页条件查询的方法
    // 三个参数：当前页，每页的记录数，条件封装对象
export function getCorpInfoPageList(page,limit,searchObj) {
    return request({
      // 后端Controller里面的路径
      url: '/corp_info/'+page+'/'+limit,
      //url: '/corpservice/corpinfo/moreCondtionPageList/'+page+'/'+limit,
      // 提交方式
      method: 'get',
      // 传递条件对象，如果传递Json数据，使用data。如果不是json，使用params : searchObj
      // params
      data: searchObj
    })
  }
  
  export function getCorpInfoId(id){
    return request({
      // 后端Controller里面的路径
      //url: '/corpservice/corpinfo/getCorpInfo/'+id,
      url: '/corp_infoById/'+id,
      // 提交方式
      method: 'get',
      // 传递条件对象，如果传递Json数据，使用data。如果不是json，使用params : searchObj
      // params
    })

  }

  export function getCorpNewsPageList(page,limit,name,searchObj){
    return request({
      // 后端Controller里面的路径
      url: '/corp_news/'+name+'/'+page+'/'+limit,
      // 提交方式
      method: 'get',
      // 传递条件对象，如果传递Json数据，使用data。如果不是json，使用params : searchObj
      // params
      data: searchObj
    })
  }

export function getEconomicNewPageList(page,limit,searchObj){
  return request({
    url: '/economic_news/'+page+'/'+limit,
    // 提交方式
    method: 'get',
    data: searchObj
  })
}

  //获取某公司所有新闻的情感分析值
  export function getCorpNewsEmotionCount(name){
    return request({
      // 后端Controller里面的路径
      url:'/corp_news_emotion/'+name,
      // 提交方式
      method: 'get',
      // 传递条件对象，如果传递Json数据，使用data。如果不是json，使用params : searchObj
      // params
    })
  }

//获取某公司风险评估图数据
  export function getCorpScore(id){
    return request({
      // 后端Controller里面的路径
      url:'/corp_news/simu/'+id,
      // 提交方式
      method: 'get',
      // 传递条件对象，如果传递Json数据，使用data。如果不是json，使用params : searchObj
      // params
    })
  }

  //获取词云图词和词频

  export function getWordsCloud(industy){
    return request({
      url:'/indu_news/keywords/'+industy,
      method:'get'
    })
  }
 
//获取哈行业新闻列表(分页)
export function getInduPageList(page,limit,industy,searchObj){
  return request({
    url: '/indu_news/'+industy+'/'+page+'/'+limit,
    method: 'get',
    data: searchObj
  })
}