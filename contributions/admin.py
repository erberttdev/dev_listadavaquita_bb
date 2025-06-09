from django.contrib import admin
from .models import Contribution

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('name', 'gift', 'amount', 'payment_status', 'created_at')
    list_filter = ('payment_status',)
    search_fields = ('name', 'email', 'cpf', 'gift__name')
    ordering = ('-created_at',)
