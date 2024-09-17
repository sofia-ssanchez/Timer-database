from django.shortcuts import render
from rest_framework import status #HTTP status codes
from rest_framework.response import Response # used to return JSON responses to HTTP requests
from rest_framework.decorators import api_view # used to specify which HTTP method a view supports (GET or POST)
from .models import User 
from .serializers import UserSerializer

# Create your views here.
# Views does the thing you want done when gone to URL

@api_view(['POST'])
def register_users(request):
    serializer = UserSerializer(data=request.data) # initializes the serializer with the data that was sent in the request
    if serializer.is_valid(): # checking if the data that was inputed is valid and handles it 
        serializer.save() # creates a new User object in db w data provided
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


