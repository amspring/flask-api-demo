# -*- coding: utf-8 -*-
# File     : __init__.py.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 16:39
# Remarks  :
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

from .. import config


def make_celery(app_name):
    celery = Celery(app_name,
                    broker=config.CELERY_BROKER_URL,
                    result_backend=config.RESULT_BACKEND)

    celery.config_from_object(config)

    celery.conf.beat_schedule = beat_schedule

    return celery


beat_schedule = {
    # 每10秒执行一次。 秒级别可以用 timedelta, 分钟级别及以上可以用 crontab
    'task-one-function': {
        'task': 'app.tasks.jobs.task_one_function',
        'schedule': timedelta(seconds=10),
        'kwargs': {
            "action": "note", "id": 100000, "msg": "每10秒执行一次"
        }
    },
    # 每周1早上8：20 分执行
    'task-two-function': {
        'task': 'app.tasks.jobs.task_two_function',
        'schedule': crontab(minute=20, hour=8, day_of_week=1),
        'kwargs': {
            "action": "live", "id": 99999, "msg": "每周1早上8：20 分执行"
        }
    }
}
