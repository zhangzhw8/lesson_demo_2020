# -*- coding: utf-8 -*-

import logging
import time

from celery.schedules import crontab
from celery.task import task, periodic_task

from moments.models import WeChatUser

logger = logging.getLogger(__name__)


@task()
def very_very_slow_add(a, b):
    """
    非常非常慢的加法函数
    """
    # 先睡10s再计算
    logger.info("好困啊，先睡会...")
    time.sleep(10)
    result = a + b
    logger.info("睡醒了！%s + %s = %s！", a, b, result)
    return result


@task()
def send_mail(client, receiver, title, content):
    """
    发送邮件
    """
    logger.info("[send mail] params: receiver(%s), title(%s), content(%s)", receiver, title, content)
    send_result = client.cmsi.send_mail({
        "receiver": receiver,
        "title": title,
        "content": content,
    })
    logger.info("[send_mail] result: %s", send_result)


def send_drink_water_mail(receiver, title, content):
    logger.info("[send mail] params: receiver(%s), title(%s), content(%s)", receiver, title, content)
    # 假装调用了发送邮件API
    logger.info("[send mail] success!")


@periodic_task(run_every=crontab(minute="*", hour="*"))
def remind_drink_water():
    logger.info("[remind drink water] start")

    for user in WeChatUser.objects.all():
        receiver = user.email
        title = f"Hey, {user.user.username}. It's time to drink water!"
        content = "Dun Dun Dun..."
        send_drink_water_mail(receiver, title, content)

    logger.info("[remind drink water] end.")

