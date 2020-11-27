# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from . import settings as weixin_settings
from .accounts import WeixinAccount
from .models import BkWeixinUser


def get_user(request):
    user = None
    user_id = request.session.get('weixin_user_id')
    if user_id:
        try:
            user = BkWeixinUser.objects.get(pk=user_id)
        except BkWeixinUser.DoesNotExist:
            user = None
    return user or AnonymousUser()


class WeixinProxyPatchMiddleware(MiddlewareMixin):
    """
    该中间件需要被放置在所有中间件之前
    解决多级Nginx代理下原始来源Host(`X-Forwarded-Host`)被下层Nginx覆盖的问题
    解决方式：单独设置一个Header，本中间件进行覆盖替换`X-Forwarded-Host`

    # django 获取Host方式
    # django.http.request +73
    def get_host(self):
        '''Returns the HTTP host using the environment or request headers.'''
        # We try three options, in order of decreasing preference.
        if settings.USE_X_FORWARDED_HOST and (
                'HTTP_X_FORWARDED_HOST' in self.META):
            host = self.META['HTTP_X_FORWARDED_HOST']
            ...
    """

    def process_request(self, request):
        if weixin_settings.USE_WEIXIN and weixin_settings.X_FORWARDED_WEIXIN_HOST in request.META:
            # patch X-Forwaded-Host header
            request.META["HTTP_X_FORWARDED_HOST"] = request.META.get(weixin_settings.X_FORWARDED_WEIXIN_HOST)


class WeixinAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Weixin authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'weixin.core.middleware.WeixinAuthenticationMiddleware'."
        )
        setattr(request, 'weixin_user', SimpleLazyObject(lambda: get_user(request)))


class WeixinLoginMiddleware(MiddlewareMixin):
    """weixin Login middleware."""

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        weixin_account = WeixinAccount()
        # 非微信路径不验证
        if not weixin_account.is_weixin_visit(request):
            return None

        # 豁免微信登录装饰器
        if getattr(view, 'weixin_login_exempt', False):
            return None

        # 验证OK
        if request.weixin_user.is_authenticated:
            return None

        # 微信登录失效或者未通过验证，直接重定向到微信登录
        return weixin_account.redirect_weixin_login(request)
