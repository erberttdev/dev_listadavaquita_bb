from django.db import models
from django.conf import settings

class Event(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Público'),
        ('private', 'Privado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    name = models.CharField('Nome do Evento', max_length=255)
    date = models.DateField('Data do Evento')
    visibility = models.CharField('Visibilidade', max_length=10, choices=VISIBILITY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
