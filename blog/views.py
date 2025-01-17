from . serializers import RegisterSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
            return Response(response)
        return Response({"msg":"invalid data!!"})