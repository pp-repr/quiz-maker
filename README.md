# Quiz maker

This project is a FastAPI-based web application containerized with Docker Compose. It includes a MySQL database, SMTP service for email functionalities, various Python libraries for authentication, database management and a simple frontend built with HTML, CSS, JavaScript, and Bootstrap.

## Features

- **FastAPI**: High-performance web framework for APIs.
- **MySQL**: Relational database for data storage.
- **Docker Compose**: Orchestrates multi-container environments.
- **Alembic**: Manages database migrations.
- **Authentication**: Secure user authentication with JWT and password hashing.
- **Email Sending**: Integrated SMTP service using `fastapi-mail` and Mailpit for testing.
- **Testing**: Includes Pytest for unit and integration testing.
- **Environment Configuration**: Managed through `.env` files for flexibility.
- **Frontend**: Built using HTML, CSS, and JavaScript.

## Requirements

- [Docker](https://www.docker.com/) installed.
- Python 3.10 or newer (for local development).
- `.env` file with the following variables configured:

```env
# Database
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
MYSQL_HOST=mysql-service
MYSQL_PORT=3306

# Email Configuration
USE_CREDENTIALS=False   # Set to True if using authenticated SMTP
MAIL_USERNAME=          # SMTP username (leave empty if USE_CREDENTIALS=False)
MAIL_PASSWORD=          # SMTP password (leave empty if USE_CREDENTIALS=False)
MAIL_FROM=mail@test.com # Default email sender

# Authentication and Security
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
ACCESS_TOKEN_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=60
SESSION_KEY=your_session_key

# Google API
GOOGLE_KEY=your_google_key

# Admin Configuration
ADMIN_NAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_admin_password
```

## Project Structure

```bash
├── app/
│   ├── auth/            # User authorization
│   ├── config/          # Config environment
│   ├── models/          # Database models
│   ├── responses/       # Response classes
│   ├── routes/          # API endpoints
│   ├── schemas/         # Request classes
│   ├── services/        # Service layer
│   ├── static/          # Html, css, js files, templates for mails, saving profile-images
│   ├── utils/           # Helper function
│   └── main.py          # Application entry point
├── alembic/             # Database migrations
├── tests/               # Unit tests in pytest (outdated)
├── alembic.ini
├── Dockerfile           # Dockerfile for FastAPI app
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## Installation

### 1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Update the `.env` file:
A default `.env` file is included in the repository. Update it with the appropriate values for your environment. Refer to the Requirements section for details on the required variables.

### 3. Build and start the services:
```bash
docker-compose up --build
```

### 4. Access the application:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Mailpit (SMTP Service): http://localhost:8025

## Running Database Migrations

### 1. Create a new migration:

```bash
docker-compose run fastapi bash -c "alembic revision --autogenerate -m 'Migration message'"
```

### 2. Apply the migration:

```bash
docker-compose run fastapi bash -c "alembic upgrade head"
```

## Libraries Used
- FastAPI: Web framework.
- SQLAlchemy: ORM for database interactions.
- Alembic: Database migrations.
- Pydantic: Data validation.
- Cryptography & Passlib: Secure password hashing.
- Python-Jose: JWT token management.
- FastAPI-Mail: Email functionality.
- Mailpit: SMTP service for testing emails.
- Pytest & HTTPx: Testing framework and HTTP client. (outdated)

## Additional Notes
- Use volumes in docker-compose.yml to persist data.
- The SMTP service (Mailpit) runs on ports 8025 (UI) and 1025 (SMTP).