"""Url patterns for core app routes.
All routes should expect and return json data.
"""

from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

# from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

from core import views


urlpatterns = [
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("token/", views.UserTokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("status/", views.api_status, name="status"),
    path("user-stats/", views.user_stats, name="user_stats"),
    path("users/", views.UserList.as_view(), name="user_list"),
    path("users/<str:pk>/", views.UserDetail.as_view(), name="user_detail"),
    path("students/", views.StudentList.as_view(), name="student_list"),
    path(
        "students/<str:pk>/",
        views.StudentDetail.as_view(),
        name="student_detail",
    ),
    path("parents/", views.ParentList.as_view(), name="parent_list"),
    path(
        "parents/<str:pk>/", views.ParentDetail.as_view(), name="parent_detail"
    ),
    path("teachers/", views.TeacherList.as_view(), name="teacher_list"),
    path(
        "teachers/<str:pk>/",
        views.TeacherDetail.as_view(),
        name="teacher_detail",
    ),
    path(
        "teachers/<str:pk>/courses/",
        views.TeacherCourses.as_view(),
        name="teacher_courses",
    ),
]
