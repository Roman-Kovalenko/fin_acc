from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя
    """
    email = models.EmailField(_('email address'), unique=True)
    surname = models.CharField(
        _('surname'), max_length=100, blank=True, null=True)
    name = models.CharField(_('name'), max_length=100, blank=True, null=True)
    patronymic = models.CharField(
        _('patronymic'), max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        fio = ' '.join(
            i for i in (self.surname, self.patronymic, self.name) if i)
        return fio or self.email

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
