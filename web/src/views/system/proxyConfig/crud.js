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
        disabled(){
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled(){
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled(){
          return !vm.hasPermissions('Delete')
        }
      }
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
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: true}},//这里放编辑表单配置
      },
      {
        title: '类型',
        key: 'type',
        search: {
          disabled: true
        },
        minWidth: 60,
        type: 'select',
        dict: {
          data: vm.dictionary('type')
        },
        form: {
          show: false,
          value: '',
          component: {
            span: 12
          }
        }
      },
      {
        title: '密码',
        key: 'password',
        minWidth: 90,
        type: 'input',
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: false}},//这里放编辑表单配置
      },

      {
        title: 'IP',
        key: 'IP',
        sortable: 'custom',
        minWidth: 90,
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: false}},//这里放编辑表单配置
        type: 'input'
      },
      {
        title: '端口',
        key: 'port',

        minWidth: 50,
        type: 'input',
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: false}},//这里放编辑表单配置
      },
      {
        title: '用户名',
        key: 'username',
        minWidth: 180,
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: false}},//这里放编辑表单配置
      },
      {
        title: '本地代理端口流量',
        key: 'local_proxy_port_traffic',
        minWidth: 110,
        type: 'input',
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: true}},//这里放编辑表单配置
      },
      {
        title: '本地代理端口',
        key: 'local_port',
        minWidth: 110,
        type: 'input',
        addForm: {component: {show: false}},//这里放添加表单配置
        editForm: {component: {disabled: false}},//这里放编辑表单配置
      },
      {
        title: '状态',
        key: 'is_active',
        search: {
          disabled: false
        },
        minWidth: 70,
        type: 'select',
        dict: {
          data: vm.dictionary('is_active')
        },
        editForm: {component: {disabled: false, show: true}},//这里放编辑表单配置
      },
      {
        title: '代理',
        key: 'description',
        show: false,
        search: {
          disabled: true
        },
        type: 'textarea',
        editForm: {component: {disabled: true, show: false}},//这里放编辑表单配置
        addForm: {
          disabled: false,
          component: {
            placeholder: '请输入内容',
            showWordLimit: true,
            maxlength: '20000',
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '备注',
        key: 'description',
        show: true,
        search: {
          disabled: true
        },
        type: 'textarea',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入内容',
            showWordLimit: true,
            maxlength: '2000',
            props: {
              type: 'textarea'
            }
          }
        }
      }
    ]
  }
}
