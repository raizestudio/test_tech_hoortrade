from rest_framework.routers import DefaultRouter
from django.urls import path
from accounts.views import CustomTokenObtainView 
from rest_framework_simplejwt.views import TokenVerifyView
router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('token/', CustomTokenObtainView.as_view(), name='multi_user_token'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
