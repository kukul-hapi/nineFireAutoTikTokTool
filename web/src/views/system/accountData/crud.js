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

          component: {
            span: 12,
            placeholder: '请输入姓名'
          }
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
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: {yxtInput: true}
          },
          component: {
            span: 12,
            pagination: true,
            props: {multiple: false}
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'proxy_address'
        }
      },

      {
        title: '素材目录',
        key: 'mari_dir',
        search: {
          show:false,
          disabled: false
        },
        minWidth: 110,
        type: 'input',
        form: {
          // rules: [
          //   {
          //     max: 20,
          //     message: '请输入正确的手机号码',
          //     trigger: 'blur'
          //   }
          // ],
          itemProps: {
            class: {yxtInput: true}
          },
          component: {
            placeholder: '请输入手机号码'
          }
        }
      }, {
        title: '更新时间',
        key: 'update_datetime',
        minWidth: 180,
        addForm: {component: {show: false}},
        form: {
        }
      },
      {
        title: '个人简介',
        key: 'pri_desc',
        type: 'radio',
        width: 70,

        form: {
          value: 1,
          component: {
            span: 12
          }
        },
        component: {props: {color: 'auto'}} // 自动染色
      },
      {
        title: '启用状态',
        key: 'is_active',
        type: 'switch',
        dict: {data: vm.dictionary('button_status_number')},// <---你一般只需写这一个字典配置
        width: 80,
        search: {
          show:false,
          disabled: false,
          component: {

          }
        },
        addForm: {
          component: {
            show:false,
            disabled: false
          }
        },
        view: {
          component: {},
          // dict: {
          //   data: vm.dictionary('button_whether_bool')
          // },
        },


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
          },
          helper: '限制文件大小不能超过500k'
        }
      }
    ]
  }
}
