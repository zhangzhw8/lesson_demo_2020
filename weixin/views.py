# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from django.forms import model_to_dict
from django.shortcuts import render

from blueapps.utils.logger import logger
from weixin.core.decorators import weixin_login_exempt


@weixin_login_exempt
def login_exempt_view(request):
    return render(request, 'weixin/index.html')


def index(request):
    """
    首页
    """
    # 蓝鲸用户
    bk_username = request.user.username
    # 微信用户
    wx_username = model_to_dict(request.weixin_user)

    logger.info('bk_username:{bk_username}, wx_username:{wx_username}'.format(
        bk_username=bk_username, wx_username=wx_username
    ))
    return render(request, "weixin/index.html")
