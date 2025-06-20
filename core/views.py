from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

class RootView(APIView):
    """
    Root view for the API.
    """
    def get(self, request, *args, **kwargs):
        return Response(
            {"detail": "Houston, we've had no problem.", "version": settings.API_VERSION}, status=200
        )
