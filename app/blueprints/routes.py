# -*- coding: utf-8 -*-
# File     : routes.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:21
# Remarks  :

from . import restful_api as route
from ..services import nav, user, task, course

# 头部
route.add_resource(nav.ApiNavigationList, '/navigations', endpoint='ApiNavigationList')
route.add_resource(nav.ApiNavigation, "/navigation", "/navigation/<int:_id>", endpoint='ApiNavigation')

# 后台任务
route.add_resource(task.ApiTaskStart, '/jobs/start', endpoint='ApiTaskStart')
route.add_resource(task.ApiTaskStatus, '/job/<string:task_id>', endpoint='ApiTaskStatus')

# 用户
route.add_resource(user.ApiUserList, '/users', endpoint='ApiUserList')
route.add_resource(user.ApiUser, "/user", "/user/<int:user_id>", endpoint='ApiUser')

# 登录.登出
route.add_resource(user.ApiLogin, "/login")
route.add_resource(user.ApiLogOut, "/logout")

# 课程
route.add_resource(course.ApiCourses, '/courses', endpoint='ApiCourses')
route.add_resource(course.ApiCourse, "/course", "/course/<int:course_id>", endpoint='ApiCourse')
route.add_resource(course.ApiCourseRelation, "/course/<int:course_id>/users", endpoint='ApiCourseRelation')
