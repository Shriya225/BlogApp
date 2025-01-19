from django.urls import path
from .views import RegisterView,LoginView,BlogView,PublicView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("blog/",BlogView.as_view()),
    path("home/",PublicView.as_view()),

]