# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 15:31
# Remarks  :

from flask_restful import abort
from ..models import User, Profile
from ..middleware.database import db


class UserRepository(object):

    def __init__(self):
        pass

    @staticmethod
    def rep_get_all(page, per_page, args) -> (list, int):
        """
        :param page:
        :param per_page:
        :param args:
        :return:
        """
        model = User.query

        if args.get("search"):
            model = model.filter(User.username.like("%" + args.get("search") + "%"))

        if args.get("gender"):
            model = model.filter(User.profile.has(gender=args.get("gender")))

        pagination = model.paginate(page, per_page, error_out=False)

        return pagination.items, pagination.total

    @staticmethod
    def rep_get(args) -> User:
        """
        :param args:
        :return:
        """
        return User.query.filter_by(**args).first()

    @staticmethod
    def rep_add(args, is_active: bool = True) -> dict:
        """
        :param args:
        :param is_active:
        :return:
        """
        try:
            user = User(
                mobile=args.get("mobile"),
                username=args.get("username"),
                passwd=args.get("password"),
                is_active=is_active
            )
            db.session.add(user)
            db.session.flush()

            profile = Profile(
                user_id=user.id,
                email=args.get("email"),
            )
            db.session.add(profile)

            db.session.commit()

            return {"id": user.id}
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))
        finally:
            db.session.rollback()

    @staticmethod
    def rep_update(_id, args) -> int:
        """
        :param _id:
        :param args:
        :return:
        """
        try:
            total = User.query.filter_by(id=_id).update(args)
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
        total = User.query.filter_by(id=_id).delete(synchronize_session=False)
        db.session.commit()
        return total

    @staticmethod
    def rep_profile_update(user_id, args) -> int:
        """
        :param user_id:
        :param args:
        :return:
        """
        try:
            total = Profile.query.filter_by(user_id=user_id).update(args)
            db.session.commit()
            return total
        except Exception as e:
            abort(http_status_code=400, messages=repr(e.orig))
