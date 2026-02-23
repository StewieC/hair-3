from django.urls import path
from . import views

urlpatterns = [
    path('', views.stylist_list, name='stylist_list'),
    path('book/<int:stylist_id>/', views.book_stylist, name='book_stylist'),
    path('register/', views.register_stylist, name='register_stylist'),
    path('register/success/', views.application_success, name='application_success'),
    path('check-application/', views.check_application, name='check_application'),
]