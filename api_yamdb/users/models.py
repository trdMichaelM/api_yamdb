from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=16,
        choices=CHOICES,
        default='user'
    )

    confirmation_code = models.CharField(_('confirmation code'),
                                         max_length=16, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_email_username'
            )
        ]
