from django.urls import path
from . import views

urlpatterns = [
    path('', views.stylist_list, name='stylist_list'),
    path('book/<int:stylist_id>/', views.book_stylist, name='book_stylist'),
]