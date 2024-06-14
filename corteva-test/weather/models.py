from django.db import models

class WeatherData(models.Model):
    """Model to store weather data for a specific date and station."""
    date = models.DateField()
    station_id = models.CharField(max_length=50)
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    precipitation = models.IntegerField()

    class Meta:
        unique_together = ('date', 'station_id')
        """Ensure unique combination of date and station ID."""

class WeatherStats(models.Model):
    """Model to store yearly weather statistics for a specific station."""
    year = models.IntegerField()
    station_id = models.CharField(max_length=50)
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)

    class Meta:
        unique_together = ('year', 'station_id')
        """Ensure unique combination of year and station ID."""
