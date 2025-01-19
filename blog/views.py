from . serializers import RegisterSerializer,LoginSerializer,BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator

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
    



class PublicView(APIView):
    def get(self,request):
        try:
            blogs=Blog.objects.all().order_by("?")
            if request.GET.get("search"):
                search_term=request.GET.get("search")
                blogs=Blog.objects.filter(Q(title__icontains=search_term)|Q(description__icontains=search_term))
            
            page_number=request.GET.get("page",1)
            paginator=Paginator(blogs,3)
            serializer=BlogSerializer(paginator.page(page_number),many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"data":{},"msg":"invalid page number"})


class BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self,request):
        try:
            blogs=Blog.objects.filter(user=request.user)
            if request.GET.get("search"):
                search_term=request.GET.get("search")
                blogs=Blog.objects.filter(Q(title__icontains=search_term)|Q(description__icontains=search_term))
            serializer=BlogSerializer(blogs,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)
            
    def post(self,request):
        print(request.user)
        serializer=BlogSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"created succesfully!!!"})
        return Response({"msg":"cannnot create blog.","error":serializer.errors})

    def patch(self,request):
        try:
            pk=request.data["id"]
            blog=Blog.objects.get(pk=pk)
        except:
            return Response({"masg":"invalid blog id"})
        
        if blog.user!=request.user:
            return Response({"msg":"u cannot update the data"})
        serializer=BlogSerializer(blog,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request):
        try:
            pk=request.data["id"]
            blog=Blog.objects.get(pk=pk)
        except:
            return Response({"masg":"invalid blog id"})
        
        if blog.user!=request.user:
            return Response({"msg":"u cannot delete the data"})
        blog.delete()
        return Response({"msg":"succesfully deleted blog!!!"})
        
    
