from django.db import models
from django.core.validators import MinValueValidator
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

    initial_amount = models.DecimalField(
        _('initial amount'),
        max_digits=50,
        decimal_places=2,
        default=0,
        validators=(MinValueValidator(0),),
        help_text=_('The amount you currently have')
    )
    # TODO: использовать в будущем
    current_amount = models.DecimalField(
        _('current amount'),
        max_digits=50,
        decimal_places=2,
        default=0
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        fio = ' '.join(
            i for i in (self.surname, self.name, self.patronymic) if i)
        return fio or self.email

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
