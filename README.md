# Health & Wellness Tracker

A full-stack web application for tracking health and wellness metrics, supporting UN SDG 3: Good Health and Well-Being.

## Features

- User registration and authentication
- Daily health entry logging (exercise, diet, mood, water intake, sleep)
- Data visualization with interactive charts
- Personalized health tips based on your entries
- Mobile-responsive design

## Tech Stack

- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript with Bootstrap
- Database: SQLite with SQLAlchemy ORM
- Charts: Chart.js

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open your browser and navigate to `http://localhost:5000`

## API Endpoints

- `GET /api/entries` - Returns all health entries for the authenticated user in JSON format

## Deployment

This app is configured for easy deployment to Render.com. Connect your GitHub repository to Render for automatic deployments.

## License

This project is created for educational purposes.
