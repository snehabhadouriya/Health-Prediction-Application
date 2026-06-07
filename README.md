# Health Prediction Application

## Overview

This is a Flask-based Health Prediction Application that allows users to manage patient health records and generate AI-powered health assessments using the Google Gemini API.

## Features

* Create, Read, Update, Delete (CRUD) patient records
* Email and Date of Birth validation
* Blood test value validation
* SQLite database integration
* AI-generated health assessment using Gemini API
* Automatic risk classification (Low, Moderate, High)
* Responsive Bootstrap user interface

## Technology Stack

* Python
* Flask
* SQLite
* HTML/CSS
* Bootstrap
* Google Gemini API

## Installation

1. Clone the repository
2. Install dependencies:

pip install -r requirements.txt

3. Add your Gemini API key
4. Run:

python app.py

## Project Workflow

1. User enters patient details and blood test values.
2. Data is validated.
3. Blood test values are sent to the Gemini API.
4. Gemini generates a health assessment and risk level.
5. Results are stored in the database.
6. Users can view, update, and delete records.

## Author
Sneha Bhadouriya
