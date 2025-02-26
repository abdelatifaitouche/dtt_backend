from rest_framework_simplejwt.tokens import Token
from api.models import * 
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = ['id' , 'username' , 'email']


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
     
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        
        return token
    


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True , required = True , validators = [validate_password])
    password2 = serializers.CharField(write_only = True , required = True)
    class Meta : 
        model = User
        fields = ['email' , 'username' , 'password' , 'password2']

    def validate(self , attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password' : 'Password Fields does not match'}
            )
        return attrs
    
    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'] , 
            email = validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CountrySerializer(serializers.ModelSerializer):
    class Meta : 
        model = Country
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Service
        fields = '__all__'

class RedevencesConditionsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = RedevencesConditions
        fields = '__all__'

class DividendesConditionsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = DividendesConditions
        fields = '__all__'

class IntrestsConditionsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = IntrestConditions
        fields = '__all__'



class ReponseTemplateSerializer(serializers.ModelSerializer):
    class Meta : 
        model = ReponseTemplate
        fields = '__all__'
