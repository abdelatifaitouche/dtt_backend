from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .Chatbot import Chatbot


chat = Chatbot("AIzaSyD9tBP0NaJ6s-vA_qEOwbBtAMu34g1tw9c")



@api_view(['GET'])
def chatbot(request , query):
    response = chat.generate(query)
    return Response({"data" : response} , status=status.HTTP_200_OK)