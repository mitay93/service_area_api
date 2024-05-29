# Service area API with Django and DRF (assessment task)

This project is a Django-based API for managing providers and service areas, with geospatial capabilities using Django's
GIS module.

## Features

- Manage providers with details like name, email, phone number, language, and currency.
- Manage service areas defined by polygons, associated with providers.
- Search for service areas containing a specific location.

## Requirements

- Docker
- Docker Compose
- Python 3.12
- Django 5.0+
- PostgreSQL with PostGIS
- [Poetry](https://python-poetry.org/) - optional

## Setup

### Local Development

1. **Clone the repository**:
    ```bash
    git clone **do not forget to put github link here**
    cd service-area-api
    ```

2. **Install dependencies**:
    ```bash
    poetry install
    ```

3. **Set up the database**:
    - Ensure PostgreSQL and PostGIS are installed and running.
    - Create a PostgreSQL database and enable PostGIS extensions.

4. **Create a `.env` file**:
    ```plaintext
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost, 127.0.0.1
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```

5. **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

### Docker Setup

1. **Build and run the Docker container**:
    ```bash
    docker-compose up --build
    ```

2. **Access the API**:
    - The API will be available at `http://localhost:8000`.
