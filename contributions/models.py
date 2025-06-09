from django.db import models
from gifts.models import Gift

class Contribution(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, related_name='contributions')
    name = models.CharField('Nome do Contribuinte', max_length=255)
    email = models.EmailField('Email do Contribuinte', blank=True, null=True)
    phone = models.CharField('Telefone', max_length=20)
    cpf = models.CharField('CPF', max_length=14)
    amount = models.DecimalField('Valor da Contribuição', max_digits=10, decimal_places=2)
    message = models.TextField('Mensagem', blank=True, null=True)
    payment_status = models.CharField('Status do Pagamento', max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contribuição de {self.name} para {self.gift.name}"
