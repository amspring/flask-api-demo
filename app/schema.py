# -*- coding: utf-8 -*-
# File     : schema.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-27 10:01
# Remarks  :

from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError, validates
from webargs.flaskparser import use_args

from .utils import is_mobile


def use_args_with(schema_cls, schema_kwargs=None, **kwargs):
    schema_kwargs = schema_kwargs or {}

    def factory(request):
        # Filter based on 'fields' query parameter
        only = request.args.get("fields", None)
        # Respect partial updates for PATCH requests
        partial = request.method == "PATCH"
        return schema_cls(
            only=only, partial=partial, context={"request": request}, **schema_kwargs
        )

    return use_args(factory, **kwargs)


class SearchSchema(Schema):
    page = fields.Int(
        missing=1,
        validate=validate.Range(min=1, max=9999),
        error_messages=dict(
            validator_failed='Maximum number of page reached.',
        ))
    per_page = fields.Int(
        missing=10,
        validate=validate.Range(min=5, max=100),
        error_messages=dict(
            validator_failed='Maximum number of per_page reached.',
        ))
    search = fields.Str()
    gender = fields.Str(missing="")

    class Meta:
        unknown = EXCLUDE


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    mobile = fields.String(required=True)
    email = fields.Email(missing="")

    @validates("mobile")
    def validate_mobile(self, value):
        if len(value) != 11:
            raise ValidationError('mobile must be 11')
        if not is_mobile(value):
            raise ValidationError('mobile must be num')


class UserUpdateSchema(Schema):
    username = fields.Str()


class NavSchema(Schema):
    title = fields.Str()
    url = fields.Str()


class LoginSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


class CourseSchema(Schema):
    title = fields.Str()


class CourseRtlSchema(Schema):
    user_id = fields.Int(required=True)
    role_id = fields.Int(missing=1)
