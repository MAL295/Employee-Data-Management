# Employee-Data-Management
This Project basically generated the employee data. This project build using DJango.

# Employee Management API

## Description

This is a Django-based REST API for managing employee data, performance records, and attendance. It includes features for:

-   Generating synthetic employee data.
-   Storing data in a PostgreSQL database.
-   Providing REST API endpoints for data access.
-   Documenting the API with Swagger.
-   Implementing rate limiting.
-   Docker and Docker Compose support.
-   Environment variable configuration.
-   Basic unit tests.
-   API usage logging.
-   Health check endpoint.
-   Data export to CSV.

## Features

-   **Employee Management:** Create, read, update, and delete employee records.
-   **Performance Tracking:** Record and retrieve employee performance reviews.
-   **Attendance Management:** Track employee attendance.
-   **Departmental Performance:** View departmental performance summaries.
-   **API Documentation:** Interactive API documentation using Swagger.
-   **Authentication:** Basic Authentication and Token Authentication.
-   **Authorization:** Django Model Permissions.
-   **Filtering and Pagination:** Filter and paginate API responses.
-   **Rate Limiting:** Prevent API abuse with throttling.
-   **Data Export:** Export employee data to CSV.
-   **Health Check:** Endpoint to monitor API health.
-   **Logging:** Log API usage and errors.
-   **Testing:** Basic unit tests.
-   **Dockerized Deployment:** Easy setup with Docker and Docker Compose.

## Technical Details

-   **Framework:** Django
-   **REST API:** Django REST Framework (DRF)
-   **Database:** PostgreSQL
-   **API Documentation:** Swagger (drf-yasg)
-   **Data Generation:** Faker
-   **Environment Management:** python-dotenv
-   **Testing:** pytest, pytest-django, coverage
-   **Containerization:** Docker, Docker Compose

## Setup

### Prerequisites

-   Python 3.9+
-   Docker (optional, for containerized deployment)
-   PostgreSQL (local or cloud instance)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd django_employee_management_api
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**

    -   Create a PostgreSQL database.
    -   Copy the `.env.example` file to `.env` and update the database settings:

        ```bash
        cp .env.example .env
        # Edit .env and set the correct database credentials
        ```

    -   Example `.env` file:

        ```
        DB_NAME=your_database_name
        DB_USER=your_database_user
        DB_PASSWORD=your_database_password
        DB_HOST=localhost
        DB_PORT=5432
        ```

5.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Generate synthetic data (optional):**

    ```bash
    python manage.py generate_data
    ```

7.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

9.  **Access the API:**

    -   API: `http://localhost:8000/api/`
    -   Swagger UI: `http://localhost:8000/swagger/`

### Docker Setup (Optional)

1.  **Ensure Docker and Docker Compose are installed.**
2.  **Copy `.env.example` to `.env` and configure database settings.**
3.  **Build and run the Docker containers:**

    ```bash
    docker-compose up --build
    ```

## Usage

-   **API Endpoints:** The API provides endpoints for managing employees, performance records, and attendance.  Refer to the Swagger documentation for details.
-   **Swagger UI:** Use Swagger to view available endpoints, request parameters, and response formats.  You can also use Swagger to make test requests.
-   **Data Export:** The `/api/employees/export_csv/` endpoint exports employee data to a CSV file.
-   **Health Check:** The `/api/employees/health/` endpoint returns a 200 OK status if the API is running.

## Testing

-   Run the unit tests:

    ```bash
    python manage.py test
    ```

## Logging

-   The application logs information and errors to the `logs/django.log` file.  Ensure the `logs` directory exists.

## Contributing

-   Contributions are welcome!  Please submit a pull request.

## License

-   [BSD License](https://opensource.org/licenses/BSD-3-Clause)