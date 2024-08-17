from django.urls import path
from . import views



urlpatterns = [
    path('latest-offers/', views.latest_offers, name='latest_offers'),
    path('items/', views.Items, name='items')
]
