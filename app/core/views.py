"""Views for the core application"""
# import json

# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import (
    # AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    # IsAdminUser,
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import (
    User,
    Student,
    Teacher,
    Parent,
)
from core.permissions import (
    NoAuth,
    IsStaffOrAdminOrReadOnly,
    IsOwnerOrStaffOrAdminOrReadOnly,
)
from core.serializers import (
    ParentSerializer,
    StudentSerializer,
    TeacherSerializer,
    TeacherCourseSerializer,
    UserSerializer,
    UserTokenObtainPairSerializer,
)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def api_status(request):
    """Returns True if api is up"""
    return Response({"detail": "API is up and running!", "status": True})


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def user_stats(request):
    """Returns the user stats"""
    scount = Student.objects.count()
    pcount = Parent.objects.count()
    tcount = Teacher.objects.count()
    return Response(
        {
            "detail": "User stats",
            "stats": {
                "teachers": tcount,
                "students": scount,
                "parents": pcount,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([])
def authenticated(request):
    """Returns True if user is authenticated"""
    if request.user.is_authenticated:
        serialized = UserSerializer(request.user)
        return Response(
            {"detail": "User is authenticated", "user": serialized.data}
        )
    return Response({"detail": "User is not authenticated", "user": None})


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserList(ListCreateAPIView):
    """List and Create a new user"""

    queryset = User.objects.all().order_by("-created")
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        data["detail"] = "Users fetched successfully"
        data["next"] = self.paginator.get_next_link()
        data["previous"] = self.paginator.get_previous_link()
        data["users"] = data.pop("results")
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = {"detail": "User created successfully", "user": serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    """User retrieve, update and delete"""

    permission_classes = [IsAuthenticated, IsOwnerOrStaffOrAdminOrReadOnly]
    serializer_class = UserSerializer

    def get(self, request, pk):
        """Retrieve a user"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found", "user": None},
                status.HTTP_404_NOT_FOUND,
            )
        serialized = UserSerializer(user)
        return Response(
            {"detail": "User Fetched", "user": serialized.data},
            status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update a user"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found", "user": None},
                status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        serialized = UserSerializer(user, data=data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {"detail": "User Updated", "user": serialized.data},
                status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "errors": serialized.errors,
                "detail": "An error occured",
                "user": None,
            },
            status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found", "user": None},
                status.HTTP_404_NOT_FOUND,
            )
        user.delete()
        return Response(
            {"detail": "User deleted", "user": None}, status.HTTP_202_ACCEPTED
        )


class StudentList(ListCreateAPIView):
    """List and create new students"""

    queryset = Student.objects.all().order_by("-created")
    serializer_class = StudentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsStaffOrAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        data["detail"] = "Students fetched successfully"
        data["next"] = self.paginator.get_next_link()
        data["previous"] = self.paginator.get_previous_link()
        data["students"] = data.pop("results")
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = {
            "detail": "Student created successfully",
            "student": serializer.data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class StudentDetail(APIView):
    """Student retrieve, update and delete"""

    permission_classes = []
    serializer_class = StudentSerializer

    def get(self, request, pk):
        """Retrieve a student"""
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student not found", "student": None},
                status.HTTP_404_NOT_FOUND,
            )
        serialized = StudentSerializer(student)
        return Response(
            {"detail": "Student Fetched", "student": serialized.data},
            status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update a student"""
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student not found", "student": None},
                status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        serialized = StudentSerializer(student, data=data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {"detail": "Student Updated", "student": serialized.data},
                status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "errors": serialized.errors,
                "detail": "An error occured",
                "student": None,
            },
            status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "Student not found", "student": None},
                status.HTTP_404_NOT_FOUND,
            )
        teacher.delete()
        return Response(
            {"detail": "Student not found", "student": None},
            status.HTTP_202_ACCEPTED,
        )


class TeacherList(ListCreateAPIView):
    """List and create new teachers"""

    queryset = Teacher.objects.all().order_by("-created")
    serializer_class = TeacherSerializer
    pagination_class = PageNumberPagination
    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        data["detail"] = "Teachers fetched successfully"
        data["next"] = self.paginator.get_next_link()
        data["previous"] = self.paginator.get_previous_link()
        data["teachers"] = data.pop("results")
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = {
            "detail": "Teacher created successfully",
            "teacher": serializer.data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class TeacherDetail(APIView):
    """Teacher retrieve, update and delete"""

    serializer_class = TeacherSerializer
    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def get(self, request, pk):
        """Retrieve a Teacher"""
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "Teacher not found", "teacher": None},
                status.HTTP_404_NOT_FOUND,
            )
        serialized = TeacherSerializer(teacher)
        return Response(
            {"detail": "Teacher Fetched", "teacher": serialized.data},
            status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update a teacher"""
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "Teacher not found", "teacher": None},
                status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        serialized = TeacherSerializer(teacher, data=data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {"detail": "Teacher Updated", "teacher": serialized.data},
                status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "errors": serialized.errors,
                "detail": "An error occured",
                "teacher": None,
            },
            status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "Teacher not found", "teacher": None},
                status.HTTP_404_NOT_FOUND,
            )
        teacher.delete()
        return Response(
            {"detail": "Teacher deleted", "teacher": None},
            status.HTTP_202_ACCEPTED,
        )


class TeacherCourses(APIView):
    """List courses for a teacher"""

    serializer_class = TeacherCourseSerializer
    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "Teacher not found", "teacher": None},
                status.HTTP_404_NOT_FOUND,
            )
        serialized = TeacherCourseSerializer(teacher)
        return Response(
            {"detail": "Teacher fetched", "teacher": serialized.data},
            status.HTTP_200_OK,
        )


class ParentList(ListCreateAPIView):
    """List and create new parents"""

    queryset = Parent.objects.all().order_by("-created")
    serializer_class = ParentSerializer
    pagination_class = PageNumberPagination
    authentication_classes = [NoAuth, JWTAuthentication]
    permission_classes = []

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        data["detail"] = "Parents fetched successfully"
        data["next"] = self.paginator.get_next_link()
        data["previous"] = self.paginator.get_previous_link()
        data["parents"] = data.pop("results")
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = {
            "detail": "Teacher created successfully",
            "teacher": serializer.data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class ParentDetail(APIView):
    """Parent retrieve, update and delete"""

    permission_classes = []
    authentication_classes = [NoAuth, JWTAuthentication]
    serializer_class = ParentSerializer

    def get(self, request, pk):
        """Retrieve a parent"""
        try:
            parent = Parent.objects.get(pk=pk)
        except Parent.DoesNotExist:
            return Response(
                {"detail": "Parent not found", "parent": None},
                status.HTTP_404_NOT_FOUND,
            )
        serialized = ParentSerializer(parent)
        return Response(
            {"detail": "Parent Fetched", "parent": serialized.data},
            status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update a Parent"""
        try:
            parent = Parent.objects.get(pk=pk)
        except Parent.DoesNotExist:
            return Response(
                {"detail": "Parent not found", "parent": None},
                status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        serialized = ParentSerializer(parent, data=data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {"detail": "Parent Updated", "parent": serialized.data},
                status.HTTP_202_ACCEPTED,
            )
        return Response(
            {
                "errors": serialized.errors,
                "detail": "An error occured",
                "parent": None,
            },
            status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        try:
            parent = Parent.objects.get(pk=pk)
        except Parent.DoesNotExist:
            return Response(
                {"detail": "Parent not found", "parent": None},
                status.HTTP_404_NOT_FOUND,
            )
        parent.delete()
        return Response(
            {"detail": "Parent deleted", "parent": None},
            status.HTTP_202_ACCEPTED,
        )
