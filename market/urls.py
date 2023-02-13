from django.urls import path
from . import views

urlpatterns = [
    path('get_images/market/', views.MarketImage.as_view())
]
