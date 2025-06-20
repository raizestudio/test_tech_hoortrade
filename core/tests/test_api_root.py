import pytest
from django.conf import settings
from django.urls import reverse


class TestApiRootView:
    """Test for the root endpoint"""

    @pytest.mark.django_db
    def test_root_view(self, client):
        url = reverse("api-root")
        response = client.get(url)

        assert response.status_code == 200
        assert response.json() == {
            "detail": "Houston, we've had no problem.",
            "api_version": settings.API_VERSION,
        }

    @pytest.mark.django_db
    def test_root_view_post(self, client):
        url = reverse("api-root")
        response = client.post(url)

        assert response.status_code == 405
        assert response.json() == {"detail": 'Method "POST" not allowed.'}
