from django.urls import include, path
from rest_framework.routers import DefaultRouter
from weather.views import WeatherViewSet

router = DefaultRouter()
router.register(r'weather', WeatherViewSet, basename='weather')
urlpatterns = [
    path("api/", include(router.urls)),
]
