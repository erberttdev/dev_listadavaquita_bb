from django.db import models
from django.conf import settings
from events.models import Event

class Gift(models.Model):
    STORE_TYPE_CHOICES = [
        ('physical', 'Física'),
        ('online', 'Online'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gifts')
    name = models.CharField('Nome do Presente', max_length=255)
    value = models.DecimalField('Valor do Presente', max_digits=10, decimal_places=2)
    store_name = models.CharField('Nome da Loja', max_length=255, blank=True, null=True)
    store_type = models.CharField('Tipo da Loja', max_length=10, choices=STORE_TYPE_CHOICES, blank=True, null=True)
    store_address_or_link = models.URLField('Endereço da Loja ou Link do Produto', blank=True, null=True)
    photo = models.ImageField('Foto do Presente', upload_to='gift_photos/', blank=True, null=True)
    product_link = models.URLField('Link do Produto', blank=True, null=True)
    priority = models.PositiveIntegerField('Prioridade', default=0)
    allow_simultaneous_contributions = models.BooleanField('Permitir contribuições simultâneas', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='gifts/', blank=True, null=True)
    anonymous_contributions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.event.name}"
