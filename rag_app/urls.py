from django.urls import path
from .views import * 



urlpatterns = [
    path('ragchain/<str:query>' , chatbot , name="chat")
]