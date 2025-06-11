from django.urls import path
from . import views

app_name = 'gifts'

urlpatterns = [
    path('evento/<int:event_pk>/presente/novo/', GiftCreateView.as_view(), name='gift_add'),
    path('add/', views.GiftCreateView.as_view(), name='gift_add'),
    path('<int:pk>/', views.GiftDetailView.as_view(), name='gift_detail'),
    path('<int:pk>/edit/', views.GiftUpdateView.as_view(), name='gift_edit'),
    path('<int:pk>/delete/', views.GiftDeleteView.as_view(), name='gift_delete'),
]
