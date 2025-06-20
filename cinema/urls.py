from rest_framework.routers import DefaultRouter

from .views import AuthorReviewViewSet, GenreViewSet, MovieReviewViewSet, MovieViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"reviews-authors", AuthorReviewViewSet, basename="author")
router.register(r"reviews", MovieReviewViewSet, basename="review")
router.register(r"genres", GenreViewSet, basename="genre")

urlpatterns = router.urls
