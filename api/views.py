from django.shortcuts import render,get_object_or_404
from api.models import * 
# Create your views here.
from api.serializers import * 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view , permission_classes
from rest_framework import generics , status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 

from .utils.email_service import verify_token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer
#hello




@api_view(['GET'])
def verify_email(request, token):
    print("from the verifcation :" , token)
    email = verify_token(token)
    print("from the verify email" , email)
    if email is None:
        return Response({'error': 'Invalid or expired token'}, status=400)

    user = get_object_or_404(User, email=email)
    user.is_active = True
    user.save()

    return Response({'message': 'Email verified successfully! You can now log in.'})
    

    




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
@permission_classes([IsAuthenticated])
def get_routes(request):
    routes = [
        'api/',
        'api/token',
        'api/token/refresh/',
        'api/countries'

    ]
    return Response({"response" : routes} , status = status.HTTP_200_OK)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries(request):
    countries = Country.objects.all()
    countries_serializer = CountrySerializer(countries , many = True)
    return Response({'Countries' : countries_serializer.data} , status=status.HTTP_200_OK)



@api_view(['POST'])
def handleServices(request):
    if request.method == 'POST' : 
        country_id = request.data.get('country_id')
        max_presence = request.data.get('max_presence')
        #check if the country is Other no DTT
            #return the default response 

        country_selected = Country.objects.get(id = country_id)

        if (country_selected.country_name == "Other (No DTT)"):
            reponse = ReponseTemplate.objects.filter(default_response = True) #we check directly the condition if its the greater or less, and return the coresponding data
            reponse_serializer = ReponseTemplateSerializer(reponse , many=True)
            return Response({'answer' : reponse_serializer.data} , status = status.HTTP_200_OK)


        country_model = Service.objects.get(country = country_id)

        

        condition = int(max_presence)> country_model.max_presences
        reponse = ReponseTemplate.objects.filter(max_presence_Superieur = condition) #we check directly the condition if its the greater or less, and return the coresponding data
        reponse_serializer = ReponseTemplateSerializer(reponse , many=True)
        return Response({'answer' : reponse_serializer.data} , status = status.HTTP_200_OK)
       
    return Response({'answer' : 'Unkown response'} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def handleRedevences(request , pk):
    if request.method == 'GET' : 
        print(request.data)
        country_id = Country.objects.get(id = pk)
        redevences_conditions = RedevencesConditions.objects.filter(country = country_id)
        redevences_conditions_serializer = RedevencesConditionsSerializer(redevences_conditions , many = True).data
        return Response({'country_conditions' : redevences_conditions_serializer } , status=status.HTTP_200_OK)
    return Response({'response' : 'No response available for your request'} , status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def handleDividendes(request , pk):
    if request.method == 'GET' : 
        print(request.data)
        country_id = Country.objects.get(id = pk)
        dividendes_condtions = DividendesConditions.objects.filter(country = country_id)
        dividendes_conditions_serializer = DividendesConditionsSerializer(dividendes_condtions , many = True).data
        return Response({'country_conditions' : dividendes_conditions_serializer } , status=status.HTTP_200_OK)
    return Response({'response' : 'No response available for your request'} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def handleIntrests(request , pk):
    if request.method == 'GET' : 
        print(request.data)
        country_id = Country.objects.get(id = pk)
        intrests_conditions = IntrestConditions.objects.filter(country = country_id)
        intrest_conditions_serializer = IntrestsConditionsSerializer(intrests_conditions , many = True).data
        return Response({'country_conditions' : intrest_conditions_serializer } , status=status.HTTP_200_OK)
    return Response({'response' : 'No response available for your request'} , status=status.HTTP_400_BAD_REQUEST)