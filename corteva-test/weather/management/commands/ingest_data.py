import os
import logging
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from weather.models import WeatherData, WeatherStats  # Import your models

class Command(BaseCommand):
    """Load weather data from files into the database"""

    def handle(self, *args, **options):
        """Handle the command execution"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='script.log'
        )

        start_time = datetime.now()
        folder_path = 'data/wx_data'

        try:
            file_list = os.listdir(folder_path)

            with transaction.atomic():
                for file_name in file_list:
                    if file_name.endswith('.txt'):
                        file_path = os.path.join(folder_path, file_name)
                        all_records = []
                        station_name = Path(file_path).stem

                        # Ensure the station exists or create it
                        weather_data_list = []
                        with open(file_path, 'r') as file:
                            for line in file:
                                data = line.strip().split('\t')
                                if '-9999' in data:
                                    continue
                                try:
                                    date = datetime.strptime(data[0], '%Y%m%d').date()
                                    max_temp = int(data[1].strip())
                                    min_temp = int(data[2].strip())
                                    precipitation = int(data[3].strip())
                                except ValueError:
                                    logging.warning(f'Skipping invalid data line: {line}')
                                    continue

                                weather_data_list.append(
                                    WeatherData(
                                        date=date,
                                        station_id=station_name,
                                        max_temp=max_temp,
                                        min_temp=min_temp,
                                        precipitation=precipitation
                                    )
                                )

                        # Bulk insert weather data records
                        WeatherData.objects.bulk_create(weather_data_list)

                        # Calculate weather stats
                        year_stats = {}
                        for weather_data in weather_data_list:
                            year = weather_data.date.year
                            if year not in year_stats:
                                year_stats[year] = {
                                    'max_temp_sum': 0,
                                    'min_temp_sum': 0,
                                    'precipitation_sum': 0,
                                    'count': 0
                                }
                            year_stats[year]['max_temp_sum'] += weather_data.max_temp
                            year_stats[year]['min_temp_sum'] += weather_data.min_temp
                            year_stats[year]['precipitation_sum'] += weather_data.precipitation
                            year_stats[year]['count'] += 1

                        # Create or update WeatherStats objects
                        weather_stats_list = []
                        for year, stats in year_stats.items():
                            avg_max_temp = stats['max_temp_sum'] / stats['count']
                            avg_min_temp = stats['min_temp_sum'] / stats['count']
                            total_precipitation = stats['precipitation_sum']
                            weather_stats_list.append(
                                WeatherStats(
                                    year=year,
                                    station_id=station_name,
                                    avg_max_temp=avg_max_temp,
                                    avg_min_temp=avg_min_temp,
                                    total_precipitation=total_precipitation
                                )
                            )

                        # Bulk create or update weather stats records
                        WeatherStats.objects.bulk_create(weather_stats_list)

                        end_time = datetime.now()
                        logging.info(f'Start time {start_time}, End time {end_time}, Inserted WeatherData Records {len(weather_data_list)}, Inserted WeatherStats Records {len(weather_stats_list)}')

        except Exception as e:
            logging.error(str(e))
            raise CommandError(str(e))
