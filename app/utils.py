# -*- coding: utf-8 -*-
# File     : utils.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 18:11
# Remarks  :

import re
import base64


def set_basic_auth_str(client_id, client_sec):
    """
    用户名密码编码成字符串
    :param client_id:
    :param client_sec:
    :return:
    """
    temp_str = client_id + ':' + client_sec

    # 转成bytes string
    b_str = temp_str.encode(encoding="utf-8")

    # base64 编码
    encode_str = base64.b64encode(b_str)

    # 解码
    # decode_str = base64.b64decode(encode_str)

    return 'Basic ' + encode_str.decode()


def check_string(pattern, text) -> bool:
    result = re.search(pattern, text)
    if result:
        return True
    else:
        return False


def is_mobile(text: str) -> bool:
    """
    检查手机号码
    :param text:
    :return:
    """
    return check_string(r"^1[3-9]\d{9}$", text)


def is_wechat(text: str) -> bool:
    """
    检查微信号
    :param text:
    :return:
    """
    return check_string(r"^[a-zA-Z]([-_a-zA-Z0-9]{5,19})+$", text)


def is_QQ(text: str) -> bool:
    """
    检查QQ号
    :param text:
    :return:
    """
    return check_string(r"^[1-9][0-9]{4,10}$", text)


def model_to_dict(obj, unselect: list = None):
    """
    Model obj convert to dict
    :param obj:
    :param unselect: filter column not display
    :return:
    """
    if not obj or "_sa_instance_state" not in obj.__dict__:
        return {}

    tmp, unselect = dict(), unselect if unselect else []

    for column in obj.__table__.columns:
        if column.name in unselect:
            continue
        if str(column.type) in ["DATETIME", "TIMESTAMP"]:
            value = getattr(obj, column.name)
            tmp[column.name] = str(value.strftime('%Y-%m-%d %H:%M')) if value else ""
        else:
            tmp[column.name] = getattr(obj, column.name)

    return tmp
