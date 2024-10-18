"""Serializers for the school app's models"""

from rest_framework import serializers

# from core.models import (
#     User,
#     Student,
#     Teacher,
#     Parent,
# )

from .models import (
    Department,
    Course,
)


class DepartmentSerializer(serializers.ModelSerializer):
    """Helper class to serialize Department objects
    Serializers must be checked with .is_valid() before saving
    """

    class Meta:
        """Meta class for the department serializer"""

        model = Department
        # Reorder this, the api response follows the fields order
        fields = [
            "id",
            "name",
            "head",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a plain new department"""
        department = Department.objects.create(**validated_data)
        return department

    def update(self, instance, validated_data):
        """Update an existing department"""
        instance.name = validated_data.get("name", instance.name)
        instance.head = validated_data.get("head", instance.teacher)
        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    """Serializes the Course model"""

    class Meta:
        """Meta class for the course serializer"""

        model = Course
        fields = [
            "id",
            "name",
            "department",
            "teacher",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"required": False},
        }

    def create(self, validated_data):
        """Create a plain new course"""
        course = Course.objects.create(**validated_data)
        return course

    def update(self, instance, validated_data):
        """Update an existing course"""
        instance.name = validated_data.get("name", instance.name)
        instance.department = validated_data.get(
            "department", instance.department
        )
        instance.teacher = validated_data.get("teacher", instance.teacher)
        instance.save()
        return instance


class DepartmentCourseSerializer(serializers.ModelSerializer):
    """Serializes the Department model with its courses"""

    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for the department serializer"""

        model = Department
        fields = [
            "id",
            "name",
            "head",
            "courses",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }
