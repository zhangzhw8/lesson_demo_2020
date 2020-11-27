# -*- coding: utf-8 -*-
from rest_framework.status import is_success
from rest_framework.renderers import JSONRenderer


class BKJSONRenderer(JSONRenderer):
    """
    符合蓝鲸接口格式规范的数据渲染器
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 获取response对象，以判断此次请求是否成功
        response = renderer_context["response"]
        if is_success(response.status_code):
            # 请求成功时，data 字段返回数据
            data = {
                "result": True,
                "message": "OK",
                "data": data,
            }
        else:
            # 请求失败时，message 字段返回失败原因
            data = {
                "result": False,
                "message": data,
                "data": None
            }
        return super(BKJSONRenderer, self).render(data, accepted_media_type, renderer_context)