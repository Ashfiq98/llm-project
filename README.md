# LLM Property Information Management

A Django CLI application that uses the Gemini 2.0 Flash Exp model to re-write and enhance property information, generate summaries, and create property ratings and reviews.

## Features

- Re-writes property titles and descriptions using Google's Gemini 2.0 Flash Exp model
- Generates property summaries using Ollama model
- Creates property ratings and reviews
- Fully containerized with Docker
- High code coverage (90% +)
- Uses PostgreSQL database
- Implements Django ORM

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- Google Cloud API key (for Gemini model) from here : https://aistudio.google.com/
- PostgreSQL

## Installation

1. First, clone and set up the Scrapy project (required for data fetching):
```bash
git clone https://github.com/Ashfiq98/scrapy-project.git
cd scrapy-project
docker compose build
docker compose up
```
 * For stopping container run:
```bash
docker compose down
```

2. Once the Scrapy project is running, clone the main project in a new terminal:
```bash
git clone https://github.com/Ashfiq98/llm-project.git
cd llm-project
```


## Running the Application

1. Ensure the Scrapy project container is running and has completed data fetching

2. Build and start the main project Docker containers:
```bash
docker compose build
docker compose up
```
3. For stopping container run:
```bash
docker compose down
```
## Project Structure

```
llm-project/
├── llm_app/
│   ├── management/
│   │   └── commands/
│   │       └── generate.py
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── apps.py
│   ├── helper.py
│   └── tests.py
├── llm_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

3. In a new terminal, run migrations:
```bash
docker-compose run django python manage.py makemigrations
docker-compose run django python manage.py migrate
```

4. Run the property information processing command:
```bash
docker exec -it django-con python manage.py generate
```

### Testing with Docker (Recommended)
Run tests inside Docker container:
```bash
# Run tests without coverage
docker-compose run django python manage.py test

# Run tests with coverage
docker-compose run django coverage run manage.py test

# Generate coverage report
docker-compose run django coverage report

# Generate HTML coverage report (optional)
docker-compose run django coverage html
```

### Local Testing (Alternative)
If you prefer to run tests locally (ensure you have all dependencies installed):
```bash
# Install required packages
pip install -r requirements.txt

# Run tests without coverage
python manage.py test

# Run tests with coverage
python -m coverage run manage.py test

# Generate coverage report
python -m coverage report
```

## Database Schema

### Property Table
- Original property information
- Updated title and description fields

### Property Summary Table
- property_id (Foreign Key)
- summary

### Property Rating Table
- property_id (Foreign Key)
- rating
- review

## Technical Details

- **Framework**: Django
- **Database**: PostgreSQL
- **Models**: Gemini 2.0 Flash Exp, Ollama
- **Container**: Docker
- **Testing**: Django Test Framework with Coverage.py
- **Data Fetching**: Scrapy project in separate container

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

If you encounter any issues:

1. Ensure Scrapy project is running and has completed data fetching
2. Ensure all environment variables are properly set in `.env`
3. Check Docker logs for both projects:
   - Scrapy project: `docker-compose logs` (in scrapy-project directory)
   - Main project: `docker-compose logs` (in llm-project directory)
4. Verify PostgreSQL connection
5. Ensure Google API key has necessary permissions
6. Check if all required ports are available
7. Make sure both Docker containers can communicate with each other

For more information or support, please open an issue in the repository.