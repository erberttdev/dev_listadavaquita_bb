from django.contrib import admin
from .models import Gift

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'value', 'priority', 'allow_simultaneous_contributions')
    list_filter = ('allow_simultaneous_contributions',)
    search_fields = ('name', 'event__name', 'store_name')
    ordering = ('priority',)
