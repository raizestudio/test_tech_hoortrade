from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import BaseUserTokenSerializer

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = BaseUserTokenSerializer
