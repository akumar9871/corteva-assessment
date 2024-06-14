from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date
from weather.models import WeatherData, WeatherStats
from weather.serializers import WeatherDataSerializer, WeatherStatsSerializer

class WeatherViewSetTests(TestCase):
    """Tests for the WeatherViewSet."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()
        self.weather_data_url = reverse('weather-list')
        
        WeatherData.objects.create(
            date=date(2024, 6, 13),
            station_id='ABC123',
            max_temp=30,
            min_temp=20,
            precipitation=5
        )

        WeatherData.objects.create(
            date=date(2024, 6, 14),
            station_id='DEF456',
            max_temp=28,
            min_temp=18,
            precipitation=10
        )
        
        WeatherStats.objects.create(
            year=2023, 
            station_id='ABC', 
            avg_max_temp=25.0, 
            avg_min_temp=15.0, 
            total_precipitation=3.5
        )
        
        WeatherStats.objects.create(
            year=2023, 
            station_id='XYZ', 
            avg_max_temp=28.0, 
            avg_min_temp=18.0, 
            total_precipitation=4.0
        )

    def test_get_weather_data_list(self):
        """Test retrieving the list of weather data."""
        response = self.client.get(self.weather_data_url)
        weather_data = WeatherData.objects.all()
        serializer = WeatherDataSerializer(weather_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_filter_weather_data_by_station_id(self):
        """Test filtering weather data by station ID."""
        url = f"{self.weather_data_url}?station_id=ABC123"
        response = self.client.get(url)
        weather_data = WeatherData.objects.filter(station_id='ABC123')
        serializer = WeatherDataSerializer(weather_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_filter_weather_data_by_date(self):
        """Test filtering weather data by date."""
        url = f"{self.weather_data_url}?date=2024-06-13"
        response = self.client.get(url)
        weather_data = WeatherData.objects.filter(date=date(2024, 6, 13))
        serializer = WeatherDataSerializer(weather_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_weather_stats_list(self):
        """Test retrieving the list of weather statistics."""
        response = self.client.get('/api/weather/stats/')
        weather_stats = WeatherStats.objects.all()
        serializer = WeatherStatsSerializer(weather_stats, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_filter_weather_stats_by_station_id(self):
        """Test filtering weather statistics by station ID."""
        response = self.client.get("/api/weather/stats/?station_id=ABC")
        weather_stats = WeatherStats.objects.filter(station_id='ABC')
        serializer = WeatherStatsSerializer(weather_stats, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_filter_weather_stats_by_year(self):
        """Test filtering weather statistics by year."""
        response = self.client.get('/api/weather/stats/?year=2023')
        weather_stats = WeatherStats.objects.filter(year=2023)
        serializer = WeatherStatsSerializer(weather_stats, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_invalid_station_id_weather_data(self):
        """Test filtering weather data with an invalid station ID."""
        url = f"{self.weather_data_url}?station_id=INVALID"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_date_weather_data(self):
        """Test filtering weather data with an invalid date."""
        url = f"{self.weather_data_url}?date=9999-99-99"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_station_id_weather_stats(self):
        """Test filtering weather statistics with an invalid station ID."""
        response = self.client.get("/api/weather/stats/?station_id=INVALID")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_year_weather_stats(self):
        """Test filtering weather statistics with an invalid year."""
        response = self.client.get('/api/weather/stats/?year=9999')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
