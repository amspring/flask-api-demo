# -*- coding: utf-8 -*-
# File     : course.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 17:02
# Remarks  :
from flask_restful import abort

from ..models import Course, CourseUser
from ..middleware.database import db


class CourseRepository(object):

    def __init__(self):
        pass

    @staticmethod
    def rep_get_all(page, per_page, args=None) -> (list, int):
        """
        :param page:
        :param per_page:
        :param args:
        :return:
        """
        if args is None:
            args = {}

        model = Course.query.filter(**args)
        pagination = model.paginate(page, per_page, error_out=False)

        return pagination.items, pagination.total

    @staticmethod
    def rep_get(args) -> Course:
        """
        :param args:
        :return:
        """
        return Course.query.filter_by(**args).first()

    @staticmethod
    def rep_add(args) -> dict:
        """
        :param args:
        :return:
        """
        try:
            item = Course(**args)
            db.session.add(item)
            db.session.commit()
            return {"id": item.id}
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))

    @staticmethod
    def rep_update(_id, args) -> int:
        """
        :param _id:
        :param args:
        :return:
        """
        try:
            total = Course.query.filter_by(id=_id).update(args)
            db.session.commit()
            return total
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))

    @staticmethod
    def rep_delete(_id) -> int:
        """
        :param _id:
        :return:
        """
        total = Course.query.filter_by(id=_id).delete(synchronize_session=False)
        db.session.commit()
        return total

    @staticmethod
    def rep_relation_all(page, per_page, course_id) -> (list, int):
        """
        课程下用户
        :param page:
        :param per_page:
        :param course_id:
        :return:
        """
        model = CourseUser.query.filter_by(deleted=False, course_id=course_id)
        pagination = model.paginate(page, per_page, error_out=False)

        return pagination.items, pagination.total

    def rep_relation_add(self, course_id, args) -> bool:
        """
        课程关联用户
        :param course_id:
        :param args:
        :return:
        """
        course = self.rep_get(dict(id=course_id))
        if not course:
            abort(404, messages=f"课程不存在.")

        rtl = CourseUser(
            role_id=args.get("role_id"),
            course_id=course_id,
            user_id=args.get("user_id"),
        )
        db.session.add(rtl)
        db.session.commit()

        return True
