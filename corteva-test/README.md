### README.md
```markdown
# Corteva Test Project
This is a Django-based web application for managing weather data.
## Project Structure
```
corteva_test/
├── corteva_test/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── weather/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   ├── migrations/
├── manage.py
├── db.sqlite3
├── script.log
├── .coverage
├── .DS_Store
└── requirements.txt
```
## Setup and Installation
### Prerequisites
- Python 3.8 or later
- pip (Python package installer)
- virtualenv (recommended)


### Installation Steps
   ```
1. **Clone the repository**
   ```bash
   git clone
   cd corteva_test
   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  #ON Mac
   venv\Scripts\activate     #On Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Migrations**
   ```bash
   python manage.py makemigrations weather
   python manage.py migrate
   ```
5. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```
6. **Ingest Data and calculate stats**
   ```bash
   python manage.py ingest_data
   ```
7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
### Access the Application
Open your web browser and go to `http://localhost:8000`.
### Accessing Swagger UI
After starting the development server, you can access the Swagger UI at:
```
http://localhost:8000/swagger/
## Usage
### Weather Data Endpoints
#### List Weather Data
- **URL**: `/weather/`
- **Method**: `GET`
- **Query Parameters**:
  - `station_id` (optional): Filter by station ID
  - `date` (optional): Filter by date (YYYY-MM-DD)
#### Retrieve Weather Stats
- **URL**: `/weather/stats/`
- **Method**: `GET`
- **Query Parameters**:
  - `station_id` (optional): Filter by station ID
  - `year` (optional): Filter by year
## Development
### Running Tests
To run the tests, use the following command:
```bash
python manage.py test
```
### Test coverage
```bash
coverage run manage.py test
```
```bash
coverage report
```
![alt text](<artifacts/Screenshot 2024-06-14 at 1.08.16 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.51.42 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.52.07 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.52.27 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.52.47 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.56.10 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.56.24 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.56.39 PM.png>)
![alt text](<artifacts/Screenshot 2024-06-14 at 12.56.47 PM.png>)







