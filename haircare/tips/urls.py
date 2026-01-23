from django.urls import path
from . import views

urlpatterns = [
    path('', views.tips_list, name='tips_list'),
    path('add/', views.add_tip, name='add_tip'),
]