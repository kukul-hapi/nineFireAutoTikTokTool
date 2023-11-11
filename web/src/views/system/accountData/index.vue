<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @selection-change="handleSelectionChange"
      v-loading="loading"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <div style="display: inline-block; margin-right: 20px;width: 1800px">
          <div style="display: inline-block; margin-right: 20px;">
            <el-dropdown type="primary" size="small" @command="handleDropdownCommand">
              <el-button type="success" size="small">
                快捷启用状态<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown" style="padding: 10px; margin-left: 5px;">
                <el-dropdown-item command="add">批量启用</el-dropdown-item>
                <el-dropdown-item command="edit">批量禁用</el-dropdown-item>
                <el-dropdown-item command="checkOut">本页启用</el-dropdown-item>
                <el-dropdown-item command="del">本页禁用</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>

          <div style="display: inline-block; margin-right: 20px;">
            <el-dropdown type="primary" size="small" @command="">
              <el-button type="info" size="small">
                批量操作<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="delList">批量删除</el-dropdown-item>
                <el-dropdown-item command="check_email">邮箱验证</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>

          <el-select id="operationSelect" v-model="value" style="display: inline-block; margin-right: 20px;"
                     >
            <el-option  v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"></el-option>
          </el-select>
          <el-button type="primary"  @click="executeOperation"><i class="el-icon-caret-right" ></i> 执行操作</el-button>

          <el-button type="warning" disabled>停止操作</el-button>
        </div>

        <el-button-group style="display: inline-block; margin-right: 20px;">
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
  name: 'user',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      options:
        [{
        value: '0',
        label: '上传视频'
      }, {
        value: '1',
        label: '邮箱注册账号'
      }, {
        value: '2',
        label: '评论区获客'
      }, {
        value: '3',
        label: '直播间获客'
      }, {
        value: '4',
        label: '批量关注'
      }, {
        value: '5',
        label: '修改账号头像'
      }, {
        value: '6',
        label: 'Google登录注册'
      }, {
        value: '7',
        label: 'Twitter登录注册'
      }, {
        value: '8',
        label: '仅登录（获取Cookie）'
      }, {
        value: '9',
        label: '读取账号详情'
      }, {
        value: '10',
        label: '修改账号资料'
      },
      ],
      value: '',
      loading: false,

    }
  },
  methods: {
    handleDropdownCommand(command) {
      // 根据用户选择的 command 执行相应的操作
      if (command === 'add') {
        this.batchEnable(); // 调用批量启用方法
      } else if (command === 'edit') {
        this.batchDisable(); // 调用批量禁用方法
      } else if (command === 'checkOut') {
        this.enableOnPage(); // 调用本页启用方法
      } else if (command === 'del') {
        this.disableOnPage(); // 调用本页禁用方法
      }
    },
    batchEnable() {
      const pageSize = this.$data["crud"]["page"]["size"];
      const page = this.$data["crud"]["page"]["current"];
      // 发送 AJAX 请求到后端执行批量启用操作
      // 这里需要根据您的后端 API 进行相应的实现
      return api.EnableListState(pageSize, page)
    },
    batchDisable() {
      const pageSize = this.$data["crud"]["page"]["size"];
      const page = this.$data["crud"]["page"]["current"];
      // 发送 AJAX 请求到后端执行批量启用操作
      // 这里需要根据您的后端 API 进行相应的实现
      return api.DisableListState(pageSize, page)
    },
    enableOnPage() {
      const pageSize = this.$data["crud"]["page"]["size"];
      const page = this.$data["crud"]["page"]["current"];
      // 发送 AJAX 请求到后端执行批量启用操作
      // 这里需要根据您的后端 API 进行相应的实现
      return api.enableOnPageState(pageSize, page)
    },
    disableOnPage() {
      const pageSize = this.$data["crud"]["page"]["size"];
      const page = this.$data["crud"]["page"]["current"];
      return api.disableOnPageState(pageSize, page)
    },
    executeOperation() {
      this.loading = true; // 在点击按钮后设置 loading 为 true
      // this.
      const selectedOperation = this.value;
      api.executeOperation(selectedOperation)
        .then(() => {
          // 请求成功后将 loading 设置为 false
          this.loading = false;
        })
        .catch((error) => {
          // 处理错误，例如显示错误提示
          console.error(error);
          this.loading = false;
        });
    },
    getCrudOptions() {
      this.crud.searchOptions.form.user_type = 0
      return crudOptions(this)
    },
    pageRequest(query) {
      return api.GetList(query)
    },
    addRequest(row) {
      return api.AddObj(row)
    },
    updateRequest(row) {
      return api.UpdateObj(row)
    },
    delRequest(row) {
      return api.DelObj(row.id)
    },
    batchDelRequest(ids) {
      return api.BatchDel(ids)
    },
    handleSelectionChange(selection) {

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
