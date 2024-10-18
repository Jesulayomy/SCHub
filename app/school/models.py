from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

from core.models import (
    Teacher,
)


class Department(models.Model):
    """Defines the department class"""

    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid4, editable=False
    )
    created = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )
    name = models.CharField(
        _("name"),
        max_length=60,
        unique=True,
    )
    head = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name="departments",
        null=True,
        default=None,
    )

    class Meta:
        """Meta class for Department model"""

        verbose_name = _("department")
        verbose_name_plural = _("departments")

    def __str__(self):
        return self.name


class Course(models.Model):
    """Defines the course class"""

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )
    name = models.CharField(
        _("name"),
        max_length=60,
        unique=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="courses",
        null=True,
        default=None,
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name="courses",
        null=True,
        default=None,
    )

    class Meta:
        """Meta class for Course model"""

        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.name
