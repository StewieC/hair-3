from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_home, name='gallery_home'),
    path('transformation/<int:transformation_id>/', views.transformation_detail, name='transformation_detail'),
    path('add/', views.add_transformation, name='add_transformation'),
    path('transformation/<int:transformation_id>/like/', views.like_transformation, name='like_transformation'),
    path('transformation/<int:transformation_id>/comment/', views.add_comment, name='add_comment'),
]