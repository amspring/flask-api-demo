# -*- coding: utf-8 -*-
# File     : auth.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:52
# Remarks  :
import random
import string
import jwt

from flask import g, request
from functools import wraps
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask_restful import Resource, abort

from .conf import settings
from .middleware.redis import cache


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        authorization = request.headers.get("Authorization")
        if not authorization:
            abort(403, messages=f"Auth token is missing in headers.")

        auth_type, token = authorization.split(None, 1)

        # 判断是否在缓存中, 有再继续往下验证
        if not cache.get(token):
            abort(401, messages=f"认证已经失效, 请重新登录获取.")

        payload = JwtToken.decode(token)
        g.user_id = payload.get("user_id")

        return func(*args, **kwargs)

    return wrapper


class BaseResource(Resource):
    """无需验证token"""

    @staticmethod
    def cache_delete(cache_list_key=None, action=None, _id=None):
        """
        当数据添加时候     -> 需要更新移除cache_list_key,
        当更新或者删除时候  -> 需要更新移除cache_list_key 和 _id
        :param cache_list_key:
        :param action:
        :param _id:
        :return:
        """
        if cache_list_key:
            cache.delete(cache_list_key)
        if action and _id:
            cache.delete_memoized(action, _id)


class AuthResource(BaseResource):
    """排除get请求需要验证token"""
    method_decorators = {
        'post': [authenticate],
        'put': [authenticate],
        'delete': [authenticate]
    }


class GetAuthResource(BaseResource):
    """全部需要验证token"""
    method_decorators = [authenticate]


class JwtToken(object):

    def encode(self, data, exp: int = settings.auth.JWT_TOKEN_EXP):
        """
        加密数据
        :param exp:
        :param data: dict
        :return:
        """
        refresh_data, temp = data, dict()

        temp["exp"] = data["exp"] = (datetime.now() + timedelta(seconds=exp)).strftime("%Y-%m-%d %H:%M:%S")
        temp["refresh_token"] = self.refresh_encode(refresh_data)
        temp["token"] = jwt.encode(data, settings.auth.JWT_TOKEN_SECRET, algorithm='HS256')

        return temp

    @staticmethod
    def decode(token):
        """
        解密数据
        :param token: 加密长字符串
        :return:
        """
        try:
            return jwt.decode(token, settings.auth.JWT_TOKEN_SECRET, algorithms='HS256')
        except jwt.exceptions.ExpiredSignatureError:
            abort(401, messages='Auth token is expired.')
        except jwt.exceptions.DecodeError:
            abort(401, messages='Auth token is corrupted.')
        except Exception as e:
            abort(403, messages=f"Signature verification failed: {str(e)}")

    @staticmethod
    def refresh_encode(data, days: int = 7):
        """
        加密数据
        :param data: dict
        :param days: int
        :return:
        """
        data["exp"] = datetime.now() + timedelta(days=days)
        return jwt.encode(data, settings.auth.JWT_REFRESH_TOKEN_SECRET, algorithm='HS256')

    @staticmethod
    def refresh_decode(refresh_token):
        """
        解密数据
        :param refresh_token: 加密长字符串
        :return:
        """
        try:
            data = jwt.decode(refresh_token, settings.auth.JWT_REFRESH_TOKEN_SECRET)
            return data if data else dict()
        except Exception as e:
            abort(403, message=f"Refresh decode failed: {str(e)}")


class PasswordServer(object):

    @staticmethod
    def generate_salt(length=20):
        return "".join(random.sample(string.ascii_letters + string.digits, length))

    @staticmethod
    def generate_password_hash(password, salt) -> str:
        """加密
        Args:
            password: 密码
            salt: 密盐
        Returns:
        """
        return pbkdf2_sha256.hash(password, rounds=12000, salt=salt.encode("utf-8"))

    @staticmethod
    def check_password_hash(password_hash, password_plain) -> bool:
        """检查密码
        Args:
            password_hash: 加密后的密码
            password_plain: 明文
        Returns:
            True or False
        """
        return pbkdf2_sha256.verify(password_plain, password_hash)
