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
    fundraising_value = models.DecimalField('Valor da Vaquinha', max_digits=10, decimal_places=2, blank=True, null=True)
    store_name = models.CharField('Nome da Loja', max_length=255, blank=True, null=True)
    store_type = models.CharField('Tipo da Loja', max_length=10, choices=STORE_TYPE_CHOICES, blank=True, null=True)
    store_address_or_link = models.URLField('Endereço da Loja ou Link do Produto', blank=True, null=True)
    photo = models.ImageField('Foto do Presente', upload_to='gift_photos/', blank=True, null=True)
    product_link = models.URLField('Link do Produto', max_length=500, blank=True, null=True)
    priority = models.PositiveIntegerField('Prioridade', default=0)
    allow_simultaneous_contributions = models.BooleanField('Permitir contribuições simultâneas', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='gifts/', blank=True, null=True)
    anonymous_contributions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.event.name}"

class CatalogProduct(models.Model):
    name = models.CharField('Nome do Produto', max_length=255)
    image_url = models.URLField('URL da Imagem', max_length=500)
    price = models.DecimalField('Preço (R$)', max_digits=10, decimal_places=2)
    affiliate_link = models.URLField('Link de Afiliado', max_length=500)

    def __str__(self):
        return self.name

class GiftList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gift_lists')
    name = models.CharField('Nome da Lista', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class GiftListItem(models.Model):
    gift_list = models.ForeignKey(GiftList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gift_list', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.gift_list.name}"
