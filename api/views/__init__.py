#!/usr/bin/python3
"""Blueprint for schub api"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/")

from api.views.admins import *  # noqa
from api.views.departments import *  # noqa
from api.views.department_courses import *  # noqa
from api.views.index import *  # noqa
from api.views.students import *  # noqa
from api.views.teachers import *  # noqa
from api.views.teacher_courses import *  # noqa
from api.views.courses import *  # noqa
