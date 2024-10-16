from django.contrib.auth.models import AnonymousUser

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


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.method in SAFE_METHODS)
        else:
            return bool(
                request.user
                and request.user.is_authenticated
                and bool(
                    str(request.user.id) in request.path
                    or request.user.is_active
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
