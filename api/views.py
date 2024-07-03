from django.shortcuts import render
from api.models import * 
# Create your views here.
from api.serializers import * 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view , permission_classes
from rest_framework import generics , status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer



@api_view(['GET' , 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        context = f'Hey {request.user} you are getting a get response'
        return Response({'response':context} , status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get['text']
        response = f'hey {request.user}, your text is {text}'
        return Response({'response' : response} , status=status.HTTP_200_OK)
    return Response({} , status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/',
        'api/token',
        'api/token/refresh/'

    ]
    return Response({"response" : routes} , status = status.HTTP_200_OK)


