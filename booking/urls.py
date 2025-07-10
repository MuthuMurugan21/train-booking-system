from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:train_id>/', views.book_ticket, name='book_ticket'),
    path('success/', views.success, name='success'),
]
