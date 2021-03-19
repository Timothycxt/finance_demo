import request from '@/utils/request'

export function login(data) {
  return request({
   // url:'vue-admin-template/user/login',
    //url: '/eduservice/teacher/login',
    //url: '/corpservice/corpinfo/login',
    url: '/corp/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
  // url:'vue-admin-template/user/info',
   // url: '/eduservice/teacher/info',
    //url: '/corpservice/corpinfo/info',
    url: '/corp/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
