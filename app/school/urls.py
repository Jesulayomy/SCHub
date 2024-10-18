"""URLs for the school app"""

from django.urls import path
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
# )

from school import views

urlpatterns = [
    path("school-stats/", views.school_stats, name="school_stats"),
    path("courses/", views.CourseList.as_view(), name="course_list"),
    path(
        "courses/<str:pk>/", views.CourseDetail.as_view(), name="course_detail"
    ),
    path(
        "departments/", views.DepartmentList.as_view(), name="department_list"
    ),
    path(
        "departments/<str:pk>/",
        views.DepartmentDetail.as_view(),
        name="department_detail",
    ),
]
