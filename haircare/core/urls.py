from django.urls import path
from .views import HomeView, quiz_submit, quiz_result

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quiz/submit/', quiz_submit, name='quiz_submit'),
    path('quiz/result/', quiz_result, name='quiz_result'),
]