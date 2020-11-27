# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers

from moments.models import WeChatUser


# class WeChatUserSerializer(serializers.Serializer):
#     user = serializers.CharField(required=True, max_length=10)
#     motto = serializers.CharField(default="")
#     region = serializers.CharField(default="")
#     email = serializers.EmailField(default="")
#
#     def create(self, validated_data):
#         """
#         创建逻辑
#         """
#         # 建议通过以下方式获取用户模型
#         user_cls = get_user_model()
#         user, is_created = user_cls.objects.get_or_create(username=validated_data["user"])
#         wechat_user = WeChatUser.objects.create(
#             user=user,
#             motto=validated_data["motto"],
#             region=validated_data["region"],
#             email=validated_data["email"]
#         )
#         return wechat_user
#
#     def update(self, instance, validated_data):
#         """
#         更新逻辑
#         """
#         # 不希望user被修改，则更新时忽略user字段
#         # 更新时可能是部分更新，因此某些字段并不是必须的
#         instance.motto = validated_data.get("motto", instance.motto)
#         instance.region = validated_data.get("region", instance.region)
#         instance.email = validated_data.get("email", instance.email)
#         instance.save()
#         return instance


class WeChatUserSerializer(serializers.ModelSerializer):
    # 不符合要求的字段可以重写
    user = serializers.CharField(required=True, max_length=10)

    class Meta:
        # 使用到的Model类
        model = WeChatUser
        # 定义显示的字段
        # fields = "__all__"
        fields = ["id", "user", "motto", "region", "email"]

    def create(self, validated_data):
        # 对 user 对象的特殊处理
        user_cls = get_user_model()
        user, is_created = user_cls.objects.get_or_create(username=validated_data["user"])
        validated_data["user"] = user
        return super(WeChatUserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # 更新时忽略user字段
        validated_data.pop("user", None)
        return super(WeChatUserSerializer, self).update(instance, validated_data)
