from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path
from api.views import * 



urlpatterns = [
    path('' , get_routes),
    path('token/' , MyTokenObtainPairView.as_view() , name='obtain token'),
    path('token/refresh/' ,TokenRefreshView.as_view() , name='refresh' ),
    path('register/' , RegisterView.as_view()),
    path('dashboard/' , dashboard),
    path('countries/' , get_countries , name='list_countries'),
    path('services/' , handleServices , name='handle services')
]