from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import (
    # GenericAPIView,
    # ListAPIView,
    ListCreateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.permissions import (
    NoAuth,
    # CanCreate,
    # IsOwnerOrAdminOrReadOnly,
    # IsStaff,
    # IsDriverOrAdminOrReadOnly,
    # IsPassengerOrAdminOrReadOnly,
)
from school.models import (
    Department,
    Course,
)

from school.serializers import (
    DepartmentSerializer,
    CourseSerializer,
)


@api_view(["GET"])
@authentication_classes([NoAuth, JWTAuthentication])
@permission_classes([])
def school_stats(request):
    """Return the number of departments and courses"""
    departments = Department.objects.count()
    courses = Course.objects.count()
    return Response(
        {
            "detail": "School statistics",
            "data": {
                "departments": departments,
                "courses": courses,
            },
        },
        status=status.HTTP_200_OK,
    )


class DepartmentList(ListCreateAPIView):
    """List all departments or create a new one"""

    queryset = Department.objects.all().order_by("-name")
    serializer_class = DepartmentSerializer
    pagination_class = PageNumberPagination
    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        print(data)
        data["detail"] = "Departments fetched successfully"
        data["next"] = self.paginator.get_next_link()
        data["previous"] = self.paginator.get_previous_link()
        data["departments"] = data.pop("results")
        return response


class DepartmentDetail(APIView):
    """Retrieve, update or delete a department instance"""

    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def get(self, request, pk):
        """Retrieve a department instance"""
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(
                {"detail": "Department not found", "department": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized = DepartmentSerializer(department)
        return Response(
            {
                "detail": "Department retrieved successfully",
                "department": serialized.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update a department instance"""
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(
                {"detail": "Department not found", "department": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized = DepartmentSerializer(department, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {
                    "detail": "Department updated successfully",
                    "department": serialized.data,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "detail": "Invalid data",
                "errors": serialized.errors,
                "department": None,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        """Delete a department instance"""
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(
                {"detail": "Department not found", "department": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        department.delete()
        return Response(
            {"detail": "Department deleted successfully", "department": None},
            status=status.HTTP_202_ACCEPTED,
        )


class CourseList(ListCreateAPIView):
    """List all courses or create a new one"""

    queryset = Course.objects.all().order_by("-name")
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        print(data)
        data["detail"] = "Courses fetched successfully"
        data["next"] = self.paginator.get_next_link()
        data["previous"] = self.paginator.get_previous_link()
        data["courses"] = data.pop("results")
        return response


class CourseDetail(APIView):
    """Retrieve, update or delete a course instance"""

    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def get(self, request, pk):
        """Retrieve a course instance"""
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found", "course": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized = CourseSerializer(course)
        return Response(
            {
                "detail": "Course retrieved successfully",
                "course": serialized.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update a course instance"""
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found", "course": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized = CourseSerializer(course, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {
                    "detail": "Course updated successfully",
                    "course": serialized.data,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "detail": "Invalid data",
                "errors": serialized.errors,
                "course": None,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        """Delete a course instance"""
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found", "course": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        course.delete()
        return Response(
            {"detail": "Course deleted successfully", "course": None},
            status=status.HTTP_202_ACCEPTED,
        )
