from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class RootView(APIView):
    """
    Root view for the API.
    """

    @extend_schema(
        operation_id="get_root",
        description="Returns a simple message indicating the API is running.",
        responses={200: {"description": "API is running"}},
    )
    def get(self, request, *args, **kwargs):
        return Response(
            {"detail": "Houston, we've had no problem.", "api_version": settings.API_VERSION}, status=200
        )
