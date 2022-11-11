# Django
from django.db import models
from django.contrib.auth.models import User


# Apps
from apps.common.models import BaseModel


class Profile(BaseModel):
    """Extendemos User model.
    Extendemos desde Django's Abstract User, se cambia el campo username
    a email y se añaden algunos campos extras.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLES = [
        ('ADMIN', 'ADMIN'),
        ('READER', 'READER'),
    ]

    role = models.CharField(
        'Rol',
        choices=ROLES,
        max_length=255,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        """Return username."""
        return self.role

    def get_short_name(self):
        """Return username."""
        return self.role
