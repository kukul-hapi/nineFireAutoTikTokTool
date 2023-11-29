import {request} from '@/api/service'
// import {dict} from "@fast-crud/fast-crud"

export const crudOptions = (vm) => {
  // util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      // rowKey: true,
      rowId: 'id'
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 240,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled() {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: []
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '备注名',
        key: 'desc_name',
        treeNode: true, // 设置为树形列
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        show: true,
        form: {
          disabled: true
        }
      },
      {
        title: '用户名',
        key: 'username',
        search: {
          disabled: true
        },
        minWidth: 100,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '账号必填项'
            }
          ],
          component: {
            placeholder: '请输入账号'
          },
          itemProps: {
            class: {yxtInput: true}
          }
        }
      },
      {
        title: '粉丝数量',
        key: 'fans_count',
          sortable: true,
        minWidth: 90,
        type: 'input',
        disabled: false,
      },
      {
        title: '播放量',
        key: 'video_count',
        sortable: 'custom',
        minWidth: 90,

        search: {
          show:false,
          disabled: false
        },
        type: 'input',
        form: {
          show:false,
          disabled: false,

        }
      },
      {
        title: '代理地址',
        key: 'proxy_address',
        search: {
          show:false,
          disabled: false
        },
        minWidth: 140,
        type: 'text',
        form: {
          show:false,
          disabled: true
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'proxy_address'
        }
      },
      {
        title: '密码',
        key: 'password',
        show:false,
        disabled: false,

        minWidth: 140,
        type: 'text',
      },
      {
        title: '素材目录',
        key: 'mari_dir',
        search: {
          show:false,
          disabled: true
        },
        minWidth: 110,
        type: 'input',
        form: {
          disabled: true,
          show:false,
        }
      }, {
        title: '更新时间',
        key: 'update_datetime',
        minWidth: 180,
        addForm: {component: {show: false}},
        form: {
          disabled: true,
          show:false,
        }
      },
      {
        title: '个人简介',
        key: 'pri_desc',
        type: 'radio',
        width: 70,

        form: {
          disabled: true,
          show:false,
        },
        component: {props: {color: 'auto'}} // 自动染色
      },
      {
        title: '启用状态',
        key: 'is_active',
        type: 'select',//switch
        width: 80,
        search: {
          show:false,
          disabled: false,
        },
        dict: {
          data: vm.dictionary('button_status_number')
        },
        addForm: {
          component: {
            show:false,
            disabled: false
          }
        }
      },
      {
        title: '状态',
        key: 'account_type',
        search: {
          disabled: false
        },
        width: 70,
        type: 'select',
        dict: {
          data: vm.dictionary('email_account_state')
        },
        form: {
          value: true,
          component: {
            span: 12
          }
        }
      },
      {
        title: '账号分类',
        key: 'account_state',
        search: {
          disabled: false
        },
        width: 70,
        type: 'select',
        form: {
          value: true,
          component: {
            span: 12
          }
        },
        dict: {
          data: vm.dictionary('email_account_type')
        }
      },
      {
        title: '说明',
        key: 'description',
        type: 'text',
        width: 260,
        align: 'left',
        form: {
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              },
              sizeLimit: 500 * 1024 // 不能超过限制
            },
            span: 24
          }

        }
      }
    ]
  }
}
