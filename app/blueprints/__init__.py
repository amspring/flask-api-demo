# -*- coding: utf-8 -*-
# File     : __init__.py.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 17:49
# Remarks  :
import json
from flask import Blueprint, make_response

from ..middleware.csrf import csrf
from ..middleware.exception import Api
from ..logger import logger

api = Blueprint("api", __name__)

restful_api = Api(catch_all_404s=True, decorators=[csrf.exempt])
restful_api.init_app(api)


@api.get("/ping")
def ping():
    return "pong"


@restful_api.representation('application/json')
def output_json(data, code, headers=None):
    """
    :param data:
    :param code:
    :param headers:
    :return:
    """
    rep = {
        "code": code,
        "messages": data.get("messages") if code != 200 else "ok",
    }

    if code != 200 and "Duplicate entry" in data.get("messages"):
        rep["messages"] = f"数据已经存在."
        rep["code"] = 400

    if code == 200:
        rep.update({"data": data})

    resp = make_response(json.dumps(rep), 200)
    resp.headers.extend(headers or {})

    return resp


@api.errorhandler(Exception)
def exception_error(error):
    """
    # 捕获异常并写入日志, 开发环境可以关掉
    :param error:
    :return:
    """
    logger.error(repr(error))
    return output_json({"messages": repr(error)}, code=500)
