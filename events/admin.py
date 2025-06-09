from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'visibility', 'user')
    list_filter = ('visibility', 'date')
    search_fields = ('name', 'user__email')
