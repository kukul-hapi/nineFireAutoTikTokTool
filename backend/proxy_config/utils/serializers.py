# -*- coding: utf-8 -*-

"""
@author: lijunchao
@contact: QQ:1638245306
@Created on: 2021/6/1 001 22:47
@Remark: 自定义序列化器
"""
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from django.utils.functional import cached_property
from rest_framework.utils.serializer_helpers import BindingDict

from proxy_config.models import DvadminSystemTiktokProxyConfig
from dvadmin.utils.serializers import CustomModelSerializer

class TiktokProxyConfigModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = DvadminSystemTiktokProxyConfig
        fields = "__all__"


class TiktokProxyConfigModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = DvadminSystemTiktokProxyConfig
        fields = '__all__'



'''
  @author: lijunchao
  @contact: 2505811377@qq.com
  @file: serializers.py
  @time: 2022/4/8 11:12
  @desc:
  '''
from proxy_config.models import DvadminSystemUserEmail
from dvadmin.utils.serializers import CustomModelSerializer


class TKUserEmailModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = DvadminSystemUserEmail
        fields = "__all__"


class TKUserEmailModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = DvadminSystemUserEmail
        fields = '__all__'
