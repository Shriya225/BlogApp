from . serializers import RegisterSerializer,LoginSerializer,BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Blog

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Account created","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"msg":"Error occured!!","data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            response=serializer.get_jwt_token(serializer.data)
            print("************","user is ",request.user)
            return Response(response)
        return Response({"msg":"invalid data!!"})
    

class BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self,request):
        blogs=Blo
 
    def post(self,request):
        print(request.user)
        serializer=BlogSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"created succesfully!!!"})
        return Response({"msg":"cannnot create blog.","error":serializer.errors})