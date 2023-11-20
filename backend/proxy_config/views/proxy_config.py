# Create your views here.
from proxy_config.models import DvadminSystemTiktokProxyConfig
from proxy_config.utils.serializers import TiktokProxyConfigModelSerializer, \
    TiktokProxyConfigModelCreateUpdateSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework import serializers
# from backend.proxy_config.models import TiktokProxyConfig
from rest_framework.decorators import action, permission_classes
from dvadmin.utils.json_response import ErrorResponse, DetailResponse

class ExportUserProfileSerializer(CustomModelSerializer):
    #     """
    #     tiktol配置导出 序列化器
    #     """
    pass


#     last_login = serializers.DateTimeField(
#         format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
#     )
#     status = serializers.SerializerMethodField(read_only=True)
#
#
#     def get_is_active(self, instance):
#         return "启用" if instance.is_active else "停用"
#
#     class Meta:
#         model = TiktokProxyConfig
#         fields = (
#             "username",
#             "IP",
#             "type",
#             "port",
#             "password",
#             "is_active",
#             "local_proxy_port_traffic",
#             "local_port"
#         )

class TiktokProxyConfigModelViewSet(CustomModelViewSet):
    """
    配置参数接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = DvadminSystemTiktokProxyConfig.objects.all()
    serializer_class = TiktokProxyConfigModelSerializer
    create_serializer_class = TiktokProxyConfigModelCreateUpdateSerializer
    update_serializer_class = TiktokProxyConfigModelCreateUpdateSerializer
    filter_fields = ['IP', 'type', 'port', 'username', 'password', 'is_active', 'local_proxy_port_traffic',
                     'local_port']
    search_fields = ['username']
    # 导出
    export_field_label = {
        "username": "用户账号",
        "IP": "IP",
        "type": "类型",
        "port": "端口",
        "password": "密码",
        "is_active": "帐号状态",
        "local_proxy_port_traffic": "本地代理端口流量统计",
        "local_port": "本地端口"
    }
    export_serializer_class = ExportUserProfileSerializer

    @action(methods=["POST"], detail=False)
    def list_add(self, request):
        data = request.data
        # 遍历数据并批量插入数据库
        results = []

        for item in data:

            # 在这里执行数据库插入操作，假设代理配置模型为 ProxyConfig
            # 以下示例代码仅供参考，您需要根据您的模型和逻辑进行适当修改
            proxy_config = DvadminSystemTiktokProxyConfig.objects.create(
                username=item['username'],
                IP=item['IP'],
                type=item['type'],
                port=item['port'],
                password=item['password'],
                is_active=item['is_active'],
            )
            result = {
                "username": proxy_config.username,
                "IP": proxy_config.IP,
                "type": proxy_config.type,
                "port": proxy_config.port,
                "password": proxy_config.password,
                "is_active": proxy_config.is_active,
            }
            results.append(result)
        return DetailResponse(data=results, msg="添加成功")