"""Models for the core app"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.conf import settings
from django.db import models
from django.db.models.signals import (
    post_save,
    #     post_init,
)
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from uuid import uuid4


class CustomUserManager(BaseUserManager):
    """Manages the creation of users and superusers"""

    def _create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        # phone_number: str,
        **extra_fields,
    ):
        """Create base user atributes
        Parameters
        ----------
        email : str
            User email address
        password : str
            User password
        first_name : str
            User first name
        last_name : str
            User last name
        phone_number : str
            User phone number
        extra_fields : dict
            Extra fields to be saved
        Example
        -------
        >>> u = _create_user(
        ...     email="johndoe@gmail.com",
        ...     password="password",
        ...     first_name="John",
        ...     last_name="Doe",
        ...     # phone_number="+2348012345678",
        ... )
        >>> u.email
        johndoe@gmail.com
        """
        if not email:
            raise ValueError(_("Email address is required"))
        if not password:
            raise ValueError(_("Password is required"))
        if not first_name:
            raise ValueError(_("First name is required"))
        if not last_name:
            raise ValueError(_("Last name is required"))
        # if not phone_number:
        #     raise ValueError(_('Phone number is required'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            # phone_number=phone_number,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        # phone_number: str,
        **extra_fields,
    ):
        """Create basic user"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email,
            password,
            first_name,
            last_name,
            # phone_number,
            **extra_fields,
        )

    def create_superuser(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        # phone_number: str,
        **extra_fields,
    ):
        """Add superuser permission"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(
            email,
            password,
            first_name,
            last_name,
            # phone_number,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    # Required fields
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid4, editable=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    email = models.EmailField(
        _("email address"), db_index=True, unique=True, max_length=255
    )
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    recovery_question = models.CharField(
        _("recovery question"), max_length=255, blank=True, null=True
    )
    recovery_answer = models.CharField(
        _("recovery answer"), max_length=1023, blank=True, null=True
    )
    # phone_number = models.CharField(
    #     _('phone number'),
    #     max_length=15
    # )
    # Optional
    # Permissions
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    # is_student = models.BooleanField(
    #     _('student status'), default=False
    # )
    # is_alumni = models.BooleanField(
    #     _('alumni status'), default=False
    # )
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    # Django Settings
    related_name = "users"
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="A user gets all permissions in each of their groups.",
        related_name="%(app_label)s_%(class)s_groups",
        related_query_name="%(app_label)s_%(class)s_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="%(app_label)s_%(class)s_user_permissions",
        related_query_name="%(app_label)s_%(class)s_user_permission",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # , 'phone_number'

    class Meta:
        """Meta class for the user model"""

        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        """String representation of the user"""
        return f"{self.last_name} {self.first_name} - {self.email}"


class Student(models.Model):
    """Student model"""

    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid4, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    age = models.IntegerField(
        _("age"),
        null=True,
        blank=True,
    )
    start_level = models.IntegerField(_("start level"), default=1)
    current_level = models.IntegerField(
        _("current level"),
        default=1,
    )
    matric_no = models.CharField(
        _("matriculation number"),
        max_length=20,
    )
    department = models.ForeignKey(
        "school.department",
        on_delete=models.SET_NULL,
        related_name="students",
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    updated = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        """Meta class for the student model"""

        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self):
        return f"{self.user}"


class Teacher(models.Model):
    """Teacher model"""

    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid4, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    updated = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        """Meta class for the teacher model"""

        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self):
        return f"{self.user}"


class Parent(models.Model):
    """Parent model"""

    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid4, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    kids = models.ManyToManyField(
        Student,
        related_name="parents",
        blank=True,
    )
    phone_number = models.CharField(_("phone number"), max_length=15)
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    updated = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        """Meta class for the parent model"""

        verbose_name = _("parent")
        verbose_name_plural = _("parents")

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
