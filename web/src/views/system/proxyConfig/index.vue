<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button
            size="small"
            v-permission="'Create'"
            type="primary"
            @click="addRow"
          >
            <i class="el-icon-plus"/> 新增
          </el-button>
          <el-button size="small" type="danger" @click="batchDelete">
            <i class="el-icon-delete"></i> 批量删除
          </el-button>
          <el-button
            size="small"
            type="warning"
            @click="onExport"
            v-permission="'Export'"
          ><i class="el-icon-download"/> 导出
          </el-button>
          <importExcel
            api="api/system/user/"
            v-permission="'Import'"
          >导入
          </importExcel>
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
      <span slot="PaginationPrefixSlot" class="prefix">
        <el-button
          class="square"
          size="mini"
          title="批量删除"
          @click="batchDelete"
          icon="el-icon-delete"
          :disabled="!multipleSelection || multipleSelection.length == 0"
        />
      </span>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import {crudOptions} from './crud'
import {d2CrudPlus} from 'd2-crud-plus'

export default {
  name: 'proxyConfig',
  mixins: [d2CrudPlus.crud],
  data() {
    return {}
  },
  methods: {
    getCrudOptions() {
      this.crud.searchOptions.form.user_type = 0
      return crudOptions(this)
    },
    pageRequest(query) {
      return api.GetList(query)
    },
    addRequest(row) {
      const inputString = row['description'];
      const lines = inputString.trim().split('\n');

      if (lines.length > 1) {
        const result = [];

        lines.forEach(line => {
          const parts = line.split(':');
          if (parts.length >= 4) {
            const newRow = {
              IP: parts[0],
              port: parts[1],
              username: parts.slice(2, parts.length - 1).join(':'),
              password: parts[parts.length - 1],
              type:row['type'],
              is_active:0,
              account_isnull:0,
              local_proxy_port_traffic:0,
              local_port:0
            };
            result.push(newRow);
          }
          if (parts.length === 2) {
            const newRow = {
              IP: parts[0],
              port: parts[1],
              username: '',
              password: '',
              type:row['type'],
              is_active:0,
              account_isnull:0,
              local_proxy_port_traffic:0,
              local_port:0
            };
            result.push(newRow);
          }
        });
        return api.AddListObj(result); // If there are multiple lines, use AddListObj
      } else if (lines.length === 1) {
        const parts = lines[0].split(':');
        if (parts.length >= 4) {
          row['IP'] = parts[0];
          row['port'] = parts[1];
          row['username'] = parts.slice(2, parts.length - 1).join(':');
          row['password'] = parts[parts.length - 1];
          row['is_active'] = 0;
          row['local_proxy_port_traffic'] = 0;
          row['local_port'] = 0;
          row['account_isnull'] = 0;
        }
        if (parts.length === 2) {
          row['IP'] = parts[0];
          row['port'] = parts[1];
          row['username'] = '';
          row['password'] = '';
          row['is_active'] = 0;
          row['local_proxy_port_traffic'] = 0;
          row['local_port'] = 0;
          row['account_isnull'] = 0;

        }
        row['description'] = '';
        return api.AddObj(row); // If there's only one line, use AddObj
      }
    },
    updateRequest(row) {
      console.log(row)
      return api.UpdateObj(row)
    },
    delRequest(row) {
      return api.DelObj(row.id)
    },
    batchDelRequest(ids) {
      return api.BatchDel(ids)
    },
    onExport() {
      const that = this
      this.$confirm('是否确认导出所有数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        const query = that.getSearch().getForm()
        return api.exportData({...query})
      })
    },

    // 部门懒加载
    loadChildrenMethod({row}) {
      return new Promise(resolve => {
        setTimeout(() => {
          const childs = [
            {
              id: row.id + 100000,
              parent: row.id,
              name: row.name + 'Test45',
              type: 'mp4',
              size: null,
              date: '2021-10-03',
              hasChild: true
            },
            {
              id: row.id + 150000,
              parent: row.id,
              name: row.name + 'Test56',
              type: 'mp3',
              size: null,
              date: '2021-07-09',
              hasChild: false
            }
          ]
          resolve(childs)
        }, 500)
      })
    }
  }
}
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
