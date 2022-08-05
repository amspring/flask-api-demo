# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 14:16
# Remarks  :
from flask import request
from datetime import datetime
from webargs.flaskparser import use_args
from flask_restful import Resource, abort

from ..conf import settings
from ..utils import model_to_dict
from ..middleware.redis import cache
from ..auth import AuthResource, JwtToken
from ..repositories.user import UserRepository
from ..schema import UserSchema, SearchSchema, UserUpdateSchema, LoginSchema


class ApiUserList(Resource):

    @use_args(SearchSchema, location="query")
    def get(self, query):
        """
        用户列表
        :return:
        """

        results, total = UserRepository.rep_get_all(page=query.get("page"),
                                                    per_page=query.get("per_page"),
                                                    args=query)

        users = []
        for row in results:
            user = model_to_dict(row, unselect=["password", "salt"])
            user["profile"] = model_to_dict(row.profile,
                                            unselect=["id", "user_id", "created_at",
                                                      "updated_at"]) if row.profile else {}
            users.append(user)

        return {"list": users, "total": total}


class ApiUser(AuthResource):

    @staticmethod
    def get(user_id):
        """
        用户详情
        :param user_id:
        :return:
        """
        user = UserRepository.rep_get(dict(id=user_id))
        if not user:
            abort(404, messages=f"ID='{user_id}' 的用户不存在")

        res = model_to_dict(user, unselect=["password", "salt"])
        res["profile"] = model_to_dict(user.profile,
                                       unselect=["id", "user_id", "created_at", "updated_at"]) if user.profile else {}

        return res

    @staticmethod
    @use_args(UserSchema, location="json", unknown=None)
    def post(args):
        """
        用户添加
        :param args:
        :return:
        """
        return UserRepository.rep_add(args)

    @staticmethod
    def delete(user_id):
        """
        用户删除
        :param user_id:
        :return:
        """
        return UserRepository.rep_delete(user_id)

    @staticmethod
    @use_args(UserUpdateSchema, location="json", unknown=None)
    def put(args, user_id):
        """
        用户修改
        :param user_id:
        :param args:
        :return:
        """
        return UserRepository.rep_update(user_id, args)


class ApiLogin(Resource):

    @staticmethod
    @use_args(LoginSchema, location="json", unknown=None)
    def post(args):
        """
        登录
        :param args:
        :return:
        """
        user = UserRepository.rep_get(dict(mobile=args.get("login")))

        if not user:
            abort(404, messages=f"查不到该账户信息.")

        if not user.verify_password(args.get("password")):
            abort(401, messages=f"输入的密码不对.")

        # 同步记录时间, IP
        UserRepository.rep_profile_update(user_id=user.id,
                                          args={"last_login_ip": request.remote_addr, "last_login_at": datetime.now()})

        # 生成 token
        res = JwtToken().encode(
            data={"user_id": user.id},
            exp=settings.auth.JWT_TOKEN_EXP
        )

        # 缓存 token 用户信息
        cache.set(res.get("token"), ApiUser.get(user.id), timeout=settings.auth.JWT_TOKEN_EXP)

        return res


class ApiLogOut(AuthResource):

    @staticmethod
    def post():
        """
        退出
        :return:
        """
        authorization = request.headers.get("Authorization")
        auth_type, token = authorization.split("Bearer ", 1)

        return cache.delete(token)
