# -*- coding: utf-8 -*-
# File     : nav.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:57
# Remarks  :
from flask import g
from webargs.flaskparser import use_args

from ..conf import settings
from ..utils import model_to_dict
from ..middleware.redis import cache
from ..repositories.nav import NavRepository
from ..schema import SearchSchema, NavSchema
from ..auth import BaseResource, AuthResource


class ApiNavigationList(BaseResource):
    def __init__(self):
        super(ApiNavigationList, self).__init__()

    @use_args(SearchSchema, location="query")
    @cache.cached(timeout=settings.cache.day, key_prefix='api:navigation:list')
    def get(self, query):
        """
        头部导航列表
        :return:
        """

        results, total = NavRepository.rep_get_all(page=query.get("page"), per_page=query.get("per_page"))

        return {"list": [model_to_dict(row) for row in results], "total": total}


class ApiNavigation(AuthResource):
    def __init__(self):
        self.cache_list_key = 'api:navigation:list'
        super(ApiNavigation, self).__init__()

    @staticmethod
    @cache.memoize(timeout=settings.cache.minute)
    def get(_id):
        """
        :param _id:
        :return:
        """
        item = NavRepository.rep_get({"id": _id})
        return model_to_dict(item)

    @use_args(NavSchema(many=True), location="json", unknown=None)
    def post(self, args):
        """
        :param args:
            [
                {
                    "title": "新闻",
                    "url": "/news"
                },
                ...
            ]
        :return:
        """
        data = [dict({"user_id": g.get("user_id")}, **n) for n in args]
        res = NavRepository.rep_bulk_add(data)
        self.cache_delete(cache_list_key=self.cache_list_key)
        return res

    @use_args(NavSchema, location="json", unknown=None)
    def put(self, args, _id):
        """
        修改
        :param _id:
        :param args:
        :return:
        """
        total = NavRepository.rep_update(_id, args)
        self.cache_delete(cache_list_key=self.cache_list_key, action=ApiNavigation.get, _id=_id)
        return total

    def delete(self, _id):
        """
        删除
        :param _id:
        :return:
        """
        total = NavRepository.rep_delete(_id)
        self.cache_delete(action=ApiNavigation.get, _id=_id)
        return total
