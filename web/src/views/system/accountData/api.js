import { request, downloadFile } from '@/api/service'
export const urlPrefix = '/api/tik_email/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: { ...query }
  })
}

export function AddObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { soft_delete: true }
  })
}

export function BatchDel (keys) {
  return request({
    url: urlPrefix + 'multiple_delete/',
    method: 'delete',
    data: { keys }
  })
}
export function EnableListState (pageSize,page) {
  return request({
    url: urlPrefix + 'enable_list/?limit='+pageSize+'&page='+page,
    method: 'post',
    data: {}
  })
}
export function DisableListState (pageSize,page) {
  return request({
    url: urlPrefix + 'disable_list/?limit='+pageSize+'&page='+page,
    method: 'post',
    data: {}
  })
}
export function enableOnPageState (pageSize,page) {
  return request({
    url: urlPrefix + 'enable_on_page/?limit='+pageSize+'&page='+page,
    method: 'post',
    data: { }
  })
}
export function disableOnPageState (pageSize,page) {
  return request({
    url: urlPrefix + 'disable_on_page/?limit='+pageSize+'&page='+page,
    method: 'post',
    data: { }
  })
}

export function executeOperation (selectedOperation) {
  return request({
    url: urlPrefix + 'selected_operation/?executeoperation='+selectedOperation,
    method: 'post',
    data: {}
  })
}


/**
 * 导出
 * @param params
 */
export function exportData (params) {
  return downloadFile({
    url: urlPrefix + 'export_data/',
    params: params,
    method: 'get'
  })
}
