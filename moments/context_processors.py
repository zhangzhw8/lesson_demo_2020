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
from weixin.core.accounts import WeixinAccount
from django.conf import settings


def basic(request):
    # 微信相关配置
    is_weixin_visit = WeixinAccount().is_weixin_visit(request)
    adapt_site_url = settings.WEIXIN_SITE_URL if is_weixin_visit else settings.SITE_URL
    return {
        'ADAPT_SITE_URL': adapt_site_url,
    }
