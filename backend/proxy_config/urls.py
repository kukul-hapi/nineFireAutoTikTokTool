'''
  @author: hongzai
  @contact: 2505811377@qq.com
  @file: urls.py
  @time: 2022/4/8 12:23
  @desc:
  '''
from rest_framework import routers

from proxy_config.views.proxy_config import TiktokProxyConfigModelViewSet
from proxy_config.views.tiktok_user_email import TKUserEmailModelViewSet

system_url = routers.SimpleRouter()
system_url.register("api/proxy_config", TiktokProxyConfigModelViewSet)
system_url.register("api/tik_email", TKUserEmailModelViewSet)

urlpatterns = [
]
urlpatterns += system_url.urls
