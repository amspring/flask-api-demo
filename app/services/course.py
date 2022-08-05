# -*- coding: utf-8 -*-
# File     : courses.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 17:01
# Remarks  :
from webargs.flaskparser import use_args
from flask_restful import Resource

from ..auth import AuthResource
from ..repositories.course import CourseRepository
from ..utils import model_to_dict
from ..schema import SearchSchema, CourseSchema, CourseRtlSchema
from ..middleware.redis import cache
from ..conf import settings


class ApiCourses(Resource):
    def __init__(self):
        super(ApiCourses, self).__init__()

    @use_args(SearchSchema, location="query")
    @cache.cached(timeout=settings.cache.day, key_prefix='api:courses:list')
    def get(self, query):
        """
        课程列表
        :return:
        """

        results, total = CourseRepository.rep_get_all(page=query.get("page"), per_page=query.get("per_page"))

        return {"list": [model_to_dict(row) for row in results], "total": total}


class ApiCourse(AuthResource):
    def __init__(self):
        self.cache_list_key = 'api:courses:list'
        super(ApiCourse, self).__init__()

    @staticmethod
    @cache.memoize(timeout=settings.cache.minute)
    def get(_id):
        """
        :param _id:
        :return:
        """
        item = CourseRepository.rep_get({"id": _id})
        return model_to_dict(item)

    @use_args(CourseSchema, location="json", unknown=None)
    def post(self, args):
        """
        :param args:
        :return:
        """
        res = CourseRepository.rep_add(args)
        self.cache_delete(self.cache_list_key)
        return res

    @use_args(CourseSchema, location="json", unknown=None)
    def put(self, args, course_id):
        """
        修改
        :param course_id:
        :param args:
        :return:
        """
        total = CourseRepository.rep_update(course_id, args)
        self.cache_delete(self.cache_list_key, ApiCourse.get, course_id)
        return total

    def delete(self, course_id):
        """
        删除
        :param course_id:
        :return:
        """
        total = CourseRepository.rep_delete(course_id)
        self.cache_delete(self.cache_list_key, ApiCourse.get, course_id)
        return total


class ApiCourseRelation(AuthResource):
    def __init__(self):
        super(ApiCourseRelation, self).__init__()

    @staticmethod
    @use_args(SearchSchema, location="query")
    def get(query, course_id):
        """
        :param query:
        :param course_id:
        :return:
        """
        results, total = CourseRepository.rep_relation_all(page=query.get("page"), per_page=query.get("per_page"),
                                                           course_id=course_id)

        _results = []
        for result in results:
            _result = model_to_dict(result, unselect=["deleted", "enabled"])
            _result["user_name"] = result.user.username
            _result["role_name"] = result.role.title
            _results.append(_result)

        return {"list": _results, "total": total}

    @use_args(CourseRtlSchema, location="json", unknown=None)
    def post(self, args, course_id):
        """
        :param args:
        :param course_id:
        :return:
        """
        res = CourseRepository().rep_relation_add(course_id, args)
        return res
