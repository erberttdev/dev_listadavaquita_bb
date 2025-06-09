from django.urls import path
from . import views

app_name = 'contributions'

urlpatterns = [
    path('contribute/<int:gift_id>/', views.ContributionCreateView.as_view(), name='contribute'),
    path('progress/<int:gift_id>/', views.ContributionProgressView.as_view(), name='progress'),
]
