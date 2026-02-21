from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('tips/', include('tips.urls')),
    path('shop/', include('shop.urls')),
    path('booking/', include('booking.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('gallery/', include('gallery.urls')), 
]