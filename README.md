Employee Productivity & Digital Wellbeing Monitoring System

A Django-based web application for tracking employee productivity and digital wellbeing, containerized with Docker and backed by PostgreSQL, with an automated CI pipeline via GitHub Actions.

Features


User registration and authentication
Productivity tracking dashboard
PostgreSQL database backend
Fully containerized with Docker & Docker Compose
Automated CI pipeline (GitHub Actions) for build/test verification on every push


Tech Stack


Backend: Python, Django
Database: PostgreSQL
Containerization: Docker, Docker Compose
CI/CD: GitHub Actions
Frontend: HTML, CSS


Getting Started

Prerequisites


Docker & Docker Compose installed


Run locally with Docker

bashgit clone https://github.com/viveknani123/employee-portal.git
cd employee-portal
docker-compose up --build

The app will be available at http://localhost:8000

Run without Docker

bashpip install -r requirements.txt
python manage.py migrate
python manage.py runserver

CI/CD

This repo uses GitHub Actions to automatically build and verify the project on every push, configured for Python 3.13. See .github/workflows/ for the pipeline definition.

Project Structure

employee_portal/   - Django project settings
wellbeing/          - Core app (productivity tracking)
templates/          - HTML templates
static/             - Static assets (CSS/JS)
Dockerfile
docker-compose.yml
requirements.txt
