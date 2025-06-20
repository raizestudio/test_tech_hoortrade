from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from accounts.views import CustomTokenObtainView, RegisterView

router = DefaultRouter()

urlpatterns = router.urls
urlpatterns += [
    path("token/", CustomTokenObtainView.as_view(), name="multi_user_token"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegisterView.as_view(), name="register"),
]
