# -*- coding: utf-8 -*-
# File     : job.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:02
# Remarks  :
from celery.result import AsyncResult

from . import make_celery

celery = make_celery(__name__)


@celery.task(bind=True)
def delay_back_function(self, x):
    """
    :param self:
    :param x:
    :return:
    """

    data = {'data': x}

    self.update_state(
        task_id=self.request.id,
        state='PROGRESS',
        meta=data
    )

    return data


def celery_get_result(task_id):
    """
    :param task_id:
    :return:
    """
    async_task = AsyncResult(id=task_id, app=celery)

    return {
        "state": async_task.state,
        "info": async_task.info
    }


@celery.task()
def task_one_function(**kwargs):
    """
    :param kwargs:
    :return:
    """
    # code here your service
    return kwargs


@celery.task()
def task_two_function(*args, **kwargs):
    """
    :param args:
    :param kwargs:
    :return:
    """
    # code here your service
    return kwargs
