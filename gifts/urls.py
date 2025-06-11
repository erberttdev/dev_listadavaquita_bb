from django.urls import path
from . import views
from .views import GiftCreateView, GiftDetailView

app_name = 'gifts'

urlpatterns = [
    path('migrations/', views.show_migrations_view, name='show_migrations'),
    path('evento/<int:event_pk>/presente/novo/', GiftCreateView.as_view(), name='gift_add'),
    path('presente/<int:pk>/', GiftDetailView.as_view(), name='gift_detail'),
    path('add/', views.GiftCreateView.as_view(), name='gift_add'),
    path('<int:pk>/', views.GiftDetailView.as_view(), name='gift_detail'),
    path('<int:pk>/edit/', views.GiftUpdateView.as_view(), name='gift_edit'),
    path('<int:pk>/delete/', views.GiftDeleteView.as_view(), name='gift_delete'),
]
