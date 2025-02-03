"""Serializers for the core app's models"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.tokens import RefreshToken

from core.models import (
    User,
    Student,
    Teacher,
    Parent,
)
from school.serializers import CourseSerializer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serialized = UserSerializer(self.user)
        data["user"] = serialized.data
        return data


class UserSerializer(serializers.ModelSerializer):
    """Helper class to serialize User objects
    Serializers must be checked with .is_valid() before saving
    """

    class Meta:
        """Meta class for the user serializer"""

        model = User
        # Reorder this, the api response follows the fields order
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "recovery_question",
            "recovery_answer",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "recovery_answer": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a plain new user"""
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data.get("password"))
        return user

    def update(self, instance, validated_data):
        """Updates users"""
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get("last_name", instance.last_name)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    """Helper class to serialize Student objects
    Serializers must be checked with .is_valid() before saving
    """

    class Meta:
        """Meta class for the student serializer"""

        model = Student
        fields = [
            "id",
            "user",
            "date_of_birth",
            "age",
            "start_level",
            "current_level",
            "matric_no",
            "department",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new Student"""
        user = validated_data.pop("user")
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        """Updates students"""
        # instance.age = validated_data.get("age", instance.age)
        instance.start_level = validated_data.get(
            "start_level", instance.start_level
        )
        instance.current_level = validated_data.get(
            "current_level", instance.current_level
        )
        instance.matric_no = validated_data.get("matric_no", instance.matric_no)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    """Helper class to serialize Teacher objects
    Serializers must be checked with .is_valid() before saving
    """

    class Meta:
        """Meta class for the student serializer"""

        model = Teacher
        fields = [
            "id",
            "user",
            "created",
            "updated",
            "department",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new Teacher"""
        user = validated_data.pop("user")
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        """Updates teachers"""
        instance.save()
        return instance


class ParentSerializer(serializers.ModelSerializer):
    """Helper class to serialize Parent objects
    Serializers must be checked with .is_valid() before saving
    """

    class Meta:
        """Meta class for the parent serializer"""

        model = Parent
        fields = [
            "id",
            "user",
            "kids",
            "phone_number",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new Parent"""
        user = validated_data.pop("user")
        kids = validated_data.pop("kids")
        parent = Parent.objects.create(user=user, **validated_data)
        parent.kids.add(*kids)
        return parent

    def update(self, instance, validated_data):
        """Updates parents"""
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.kids.add(validated_data.get("kids", None))
        instance.save()
        return instance


class TeacherCourseSerializer(serializers.ModelSerializer):
    """Helper class to serialize Teacher objects
    Serializers must be checked with .is_valid() before saving
    """

    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for the student serializer"""

        model = Teacher
        fields = [
            "id",
            "user",
            "courses",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }
