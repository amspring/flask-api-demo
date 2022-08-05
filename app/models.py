# -*- coding: utf-8 -*-
# File     : models.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 16:51
# Remarks  :
from datetime import datetime

from .auth import PasswordServer
from .middleware.database import db


class IdMixMin(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class StatusMixin(db.Model):
    __abstract__ = True

    enabled = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)


class TimeMixMin(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(IdMixMin, StatusMixin, TimeMixMin):
    __tablename__ = "tb_user"
    __table_args__ = {'comment': '用户表'}

    mobile = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(20))
    username = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    profile = db.relationship('Profile', backref=db.backref('back_user_profile'), uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"username={self.username})>"

    @property
    def passwd(self):
        raise AttributeError('password is not a readable attribute')

    @passwd.setter
    def passwd(self, passwd):
        self.salt = PasswordServer.generate_salt()
        self.password = PasswordServer.generate_password_hash(str(passwd), self.salt)

    def verify_password(self, passwd):
        return PasswordServer.check_password_hash(self.password, passwd)


class Profile(IdMixMin, TimeMixMin):
    __tablename__ = "tb_user_profile"
    __table_args__ = {'comment': '用户详情表'}

    email = db.Column(db.String(128))
    qq = db.Column(db.String(50))
    chat = db.Column(db.String(50))
    gender = db.Column(db.Enum("man", "woman"), default="man")
    address = db.Column(db.String(255))
    signature = db.Column(db.String(512))  # 个性签名
    country = db.Column(name='country', type_=db.String(50))
    city = db.Column(name='city', type_=db.String(50))
    last_login_ip = db.Column(db.String(64))  #
    last_login_at = db.Column(db.DateTime)  # 最后登录时间
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"<Profile (id={self.id}, " \
               f"user_id={self.user_id})>"


class Nav(IdMixMin, StatusMixin, TimeMixMin):
    __tablename__ = "tb_navigation"
    __table_args__ = {'comment': '头部表'}

    title = db.Column(db.String(128), unique=True)
    url = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'))
    user = db.relationship('User')

    def __repr__(self):
        return f"<Nav(id={self.id}, " \
               f"title={self.title})>"


class Course(IdMixMin, StatusMixin, TimeMixMin):
    __tablename__ = "tb_course"
    __table_args__ = {'comment': '课程表'}

    title = db.Column(db.String(128))


class CourseUser(StatusMixin, TimeMixMin):
    __tablename__ = 'tb_course_user'
    __table_args__ = {'comment': '课程用户表'}

    role_id = db.Column(db.Integer, db.ForeignKey('tb_role.id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'), primary_key=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('tb_course.id'), primary_key=True, nullable=False, index=True)
    user = db.relationship('User')
    role = db.relationship('Role')


class Role(IdMixMin):
    __tablename__ = "tb_role"
    __table_args__ = {'comment': '角色表'}

    title = db.Column(db.String(128))
