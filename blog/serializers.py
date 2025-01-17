from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","email","password"]
    def create(self, validated_data):
        pwd=validated_data.pop("password")
        user=User.objects.create(**validated_data)
        user.set_password(pwd)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def get_jwt_token(self,data):
        user=authenticate(username=data["username"],password=data["password"])
        if not user:
            return {"msg":"invalid credentials"}
        refresh=RefreshToken.for_user(user)
        return {"msg":"logged in !!","data":{
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }}


