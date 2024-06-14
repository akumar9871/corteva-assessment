from rest_framework.response import Response
from rest_framework import generics, pagination
from weather.models import WeatherData, WeatherStats
from weather.serializers import WeatherDataSerializer, WeatherStatsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomPagination(pagination.PageNumberPagination):
    """Custom pagination settings for weather data."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WeatherViewSet(GenericViewSet, ListModelMixin):
    """View set for listing and retrieving weather data and statistics."""
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="List weather data with optional filtering by station_id and date.",
        manual_parameters=[
            openapi.Parameter('station_id', openapi.IN_QUERY, description="Filter by station ID", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date", type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request):
        """List weather data with optional filters."""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            station_id = request.GET.get('station_id')
            date = request.GET.get('date')
            if station_id:
                queryset = queryset.filter(station_id=station_id)
                if not queryset.count():
                    raise ValueError(f'station_id {station_id} not found in database.')
            if date:
                queryset = queryset.filter(date=date)
                if not queryset.count():
                    raise ValueError(f'date {date} not found in database.')

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve weather statistics with optional filtering by station_id and year.",
        manual_parameters=[
            openapi.Parameter('station_id', openapi.IN_QUERY, description="Filter by station ID", type=openapi.TYPE_STRING),
            openapi.Parameter('year', openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_STRING),
        ],
    )
    @action(methods=['get'], detail=False, url_path='stats')
    def get_weather_stats(self, request):
        """Retrieve weather statistics with optional filters."""
        try:
            queryset = WeatherStats.objects.all()

            station_id = request.query_params.get('station_id')
            year = request.query_params.get('year')

            if station_id:
                queryset = queryset.filter(station_id=station_id)
                if not queryset.count():
                    raise ValueError(f'station_id {station_id} not found in database.')
            if year:
                queryset = queryset.filter(year=year)
                if not queryset.count():
                    raise ValueError(f'year {year} not found in database.')

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = WeatherStatsSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = WeatherStatsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
