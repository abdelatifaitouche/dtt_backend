from rest_framework_simplejwt.tokens import Token
from api.models import * 
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .utils.email_service import email_verification
from rest_framework.exceptions import AuthenticationFailed




class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = ['id' , 'username' , 'email']


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['full_name'] = user.profile.full_name  # Ensure profile exists
        token['username'] = user.username
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user  # ✅ This works because `TokenObtainPairSerializer` sets `self.user`
        if not user.is_active:
            raise AuthenticationFailed('Email not verified. Please check your inbox.', code='authorization')

        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    accepted_terms = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'accepted_terms']

    def validate(self, attrs):
        # Ensure passwords match first
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match"})

        # Ensure terms are accepted
        if not attrs.get('accepted_terms', False):
            raise serializers.ValidationError({"accepted_terms": "You must accept the terms and conditions to register."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 since it's not in the model
        accepted_terms = validated_data.pop('accepted_terms')  # Extract and remove from data

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            accepted_terms=accepted_terms  # Explicitly set accepted_terms
        )
        user.set_password(validated_data['password'])  # Hash password
        user.save()

        #send an email confirmation
        response = email_verification(validated_data['email'])
        print(response)

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
