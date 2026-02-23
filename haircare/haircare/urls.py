from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('tips/', include('tips.urls')),
    path('shop/', include('shop.urls')),
    path('booking/', include('booking.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('gallery/', include('gallery.urls')), 
    path('calendar/', include('scheduler.urls')),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
]