from django.contrib.auth.models import AnonymousUser
from django.urls import resolve
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

# from core.models import User


class NoAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method == "POST":
            return (AnonymousUser(), None)
        return (AnonymousUser(), None)


class CanCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.method in SAFE_METHODS)
        else:
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.is_superuser
            )


class IsStaffOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.method in SAFE_METHODS)
        else:
            return bool(
                request.user
                and request.user.is_authenticated
                and bool(request.user.is_staff or request.user.is_superuser)
            )


class IsOwnerOrStaffOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.method in SAFE_METHODS)
        else:
            path_args = resolve(request.path_info).kwargs
            path_id = path_args.get("pk")
            print(path_id)
            print(request.user.id)
            return bool(
                request.user
                and request.user.is_authenticated
                and bool(
                    str(request.user.id) == path_id
                    or request.user.is_staff
                    or request.user.is_superuser
                    or path_id in [kid.id for kid in request.user.kids]
                )
            )


# class IsDriverOrAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return bool(request.method in SAFE_METHODS)
#         else:
#             try:
#                 driver_id = request.user.driver.id
#             except (User.driver.RelatedObjectDoesNotExist, AttributeError):
#                 return False
#             return bool(
#                 request.user and
#                 request.user.is_authenticated and
#                 bool(
#                     str(driver_id) in request.path or
#                     request.user.is_superuser
#                 )
#             )

# class IsPassengerOrAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return bool(request.method in SAFE_METHODS)
#         else:
#             try:
#                 passenger_id = request.user.passenger.id
#             except (User.passenger.RelatedObjectDoesNotExist, AttributeError):
#                 return False
#             return bool(
#                 request.user and
#                 request.user.is_authenticated and
#                 bool(
#                     str(passenger_id) in request.path or
#                     request.user.is_superuser
#                 )
#             )
