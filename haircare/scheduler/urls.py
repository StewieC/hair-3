from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_home, name='calendar_home'),
    path('add/', views.add_schedule, name='add_schedule'),
    path('edit/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('complete/<int:schedule_id>/', views.mark_completed, name='mark_completed'),
    path('history/', views.schedule_history, name='schedule_history'),
]