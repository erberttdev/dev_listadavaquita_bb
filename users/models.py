from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    full_name = models.CharField(_('Nome Completo'), max_length=150)
    cpf = models.CharField(_('CPF'), max_length=14, unique=True)
    birth_date = models.DateField(_('Data de Nascimento'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'cpf', 'birth_date']

    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.email
