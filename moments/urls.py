"""wechat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.routers import DefaultRouter

from moments.views import show_user, show_status, submit_post, friend, register, update_user, like, comment, \
    delete_comment, WeChatUserViewSet

# 定义 ViewSet 的路由
router = DefaultRouter()
router.register(r'users', WeChatUserViewSet, basename='user')

urlpatterns = [
    # 与顶层 admin 路由冲突，因此将该行注释掉
    # path('admin/', admin.site.urls),

    # 首页直接进入朋友圈列表页
    # path('', LoginView.as_view(template_name="moments/homepage.html")),
    path('', show_status),

    path('user', show_user),
    path('status', show_status),
    path('post', submit_post),
    path('friends', friend),

    # 退出登陆和注册逻辑由蓝鲸PaaS平台接管，将其注释
    # path('exit', LogoutView.as_view(next_page="/")),
    # path('register', register),

    path('update', update_user),
    path('like', like),
    path('comment', comment),
    path('comment/delete', delete_comment)
]

# 增加 User 相关的路由
urlpatterns += router.urls
