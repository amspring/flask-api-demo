# -*- coding: utf-8 -*-
# File     : task.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:51
# Remarks  :
from webargs.flaskparser import use_args
from flask_restful import Resource

from ..schema import SearchSchema

from ..tasks.jobs import delay_back_function, celery_get_result


class ApiTaskStart(Resource):
    def __init__(self):
        super(ApiTaskStart, self).__init__()

    @use_args(SearchSchema, location="query")
    def get(self, query):
        """
        countdown : 等待一段时间再执行;
        test_task.apply_async((2,3), countdown=5)

        eta : 定义任务的开始时间.这里的时间是UTC时间,这里有坑, eta = datetime.utc.now() + timedelta(seconds=10)
        test_task.apply_async((2,3), eta=now + timedelta(second=10))

        expires : 设置超时时间.
        test_task.apply_async((2,3), expires=60)

        retry : 定时如果任务失败后, 是否重试.
        test_task.apply_async((2,3), retry=False)

        retry_policy : 重试策略.
    　　max_retries : 最大重试次数, 默认为 3 次.
    　　interval_start : 重试等待的时间间隔秒数, 默认为 0 , 表示直接重试不等待.
    　　interval_step : 每次重试让重试间隔增加的秒数, 可以是数字或浮点数, 默认为 0.2
    　　interval_max : 重试间隔最大的秒数, 即 通过 interval_step 增大到多少秒之后, 就不在增加了, 可以是数字或者浮点数, 默认为 0.2 .
        :return:
        """
        task = delay_back_function.apply_async(
            args=(query.get("search"),),
            expires=60
        )

        return {
            "task_id": task.id,
            "state": task.state
        }


class ApiTaskStatus(Resource):
    def __init__(self):
        super(ApiTaskStatus, self).__init__()

    @staticmethod
    def get(task_id):
        """
        :param task_id:
        :return:
            "state": "PENDING", "PROGRESS", "SUCCESS
        """
        res = celery_get_result(task_id)
        # code here, res.state
        return res
