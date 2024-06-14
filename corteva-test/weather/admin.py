from django.contrib import admin
from .models import WeatherData, WeatherStats

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'station_id', 'max_temp', 'min_temp', 'precipitation')
    list_filter = ('station_id', 'date')
    search_fields = ('station_id',)

@admin.register(WeatherStats)
class WeatherStatsAdmin(admin.ModelAdmin):
    list_display = ('year', 'station_id', 'avg_max_temp', 'avg_min_temp', 'total_precipitation')
    list_filter = ('station_id', 'year')
    search_fields = ('station_id',)



