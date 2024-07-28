from django.shortcuts import render
from api.models import * 
# Create your views here.
from api.serializers import * 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view , permission_classes
from rest_framework import generics , status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 



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
        print(request.data)
        country_id = request.data.get('country_id')
        max_presence = request.data.get('max_presence')
        country_model = Service.objects.get(country = country_id)
        greater_answer = f"""
        According to Algeria - {country_model.country}  DTT rules, the staff presence duration exceeding  days implies the registration 
                of a Permanent Establishment in Algeria which makes the service taxable by the Algerian tax authority.
                \n
                The supplier is liable to register the PE with the tax authorities, under the Common Tax Regime in accordance with the practice in force, which should be mentioned on contract.\n
                Although suppliers in general avoid the registration of a PE, and prefer to opt for the withholding tax regime and to gross up the amount of the transaction (which is prohibited by Art. 31 of the 2009 Complementary Finance Law),\n          
    """

        less_answer = f"""
        1) It is recommended to mention on the contract that << The service will be exempt from WHT in Algeria and taxed in {country_model.country} , in accordance with Algeria - {country_model.country} DTT rules >>.\n\n
        2) A copy of the Tax Residence Certificate should be included in the payment file submitted to the tax authorities.\n

    """

        
        if int(max_presence) > country_model.max_presences :  
            return Response({'answer' : greater_answer} , status = status.HTTP_200_OK)
        else : 
            return Response({'answer' : less_answer} , status = status.HTTP_200_OK)
    return Response({'answer' : 'Unkown response'} , status=status.HTTP_400_BAD_REQUEST)



#i want to send the country and max_presence
    #get the data 
        #find the service with the country info
            #compare both max presence and country presence
                #return a coresponding response

"""
the payload should be like this : 
{
"country_id" : 2 , 
"max_presence" : 180
}

"""


#remembre in the front end that you just have to create a state variable that will hold the id : const [id , setId] = useState(null)
#then send a get request to this url https://domain.com/api/redevences/id

@api_view(['GET'])
def handleRedevences(request , pk):
    if request.method == 'GET' : 
        print(request.data)
        country_id = Country.objects.get(id = pk)
        redevences_conditions = RedevencesConditions.objects.filter(country = country_id)
        redevences_conditions_serializer = RedevencesConditionsSerializer(redevences_conditions , many = True).data
        return Response({'country_conditions' : redevences_conditions_serializer } , status=status.HTTP_200_OK)
    return Response({'response' : 'No response available for your request'} , status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def handleDividendes(request , pk):
    if request.method == 'GET' : 
        print(request.data)
        country_id = Country.objects.get(id = pk)
        dividendes_condtions = DividendesConditions.objects.filter(country = country_id)
        dividendes_conditions_serializer = DividendesConditionsSerializer(dividendes_condtions , many = True).data
        return Response({'country_conditions' : dividendes_conditions_serializer } , status=status.HTTP_200_OK)
    return Response({'response' : 'No response available for your request'} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def handleIntrests(request , pk):
    if request.method == 'GET' : 
        print(request.data)
        country_id = Country.objects.get(id = pk)
        intrests_conditions = IntrestConditions.objects.filter(country = country_id)
        intrest_conditions_serializer = IntrestsConditionsSerializer(intrests_conditions , many = True).data
        return Response({'country_conditions' : intrest_conditions_serializer } , status=status.HTTP_200_OK)
    return Response({'response' : 'No response available for your request'} , status=status.HTTP_400_BAD_REQUEST)