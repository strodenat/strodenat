# Portfolio Website with Python Game

This is my portfolio website showcasing my projects and skills. The website includes a Python game that is hosted using Flask.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)

## About
This portfolio website is designed to showcase my projects, skills, and experiences. It includes a section where visitors can play a Python game that I developed. The game is hosted using Flask, a lightweight WSGI web application framework.

## Features
- Home page with an introduction and overview of my skills.  
- Projects page displaying various projects I've worked on.  
- Game section where visitors can play a Python game.  
- Contact form for visitors to reach out to me.

## Technologies Used
- HTML, CSS, JavaScript for the front-end.  
- Flask for the back-end.  
- Python for the game logic.  
- Deployed using a suitable web server.

## Installation
1. Clone the repository:
2. ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ``

3. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set the Flask app environment variable:
    ```bash
    export FLASK_APP=app.py  # On Windows, use `set FLASK_APP=app.py`
    ```

6. Run the Flask application:
    ```bash
    flask run
    ```

7. Open your browser and go to `http://127.0.0.1:5000` to view the website.

## Usage
- Navigate through the various sections to learn more about my skills and projects.  
- Play the Python game hosted on the site by visiting the game section.  
- Use the contact form to get in touch with me.

## Folder Structure
- `portfolio-website/`
  - `__pycache__/` - Cache files
  - `game/` - Python game files
  - `static/` - Static files (CSS, JavaScript, images)
  - `templates/` - HTML templates
  - `app.py` - Flask application file
  - `Procfile` - Procfile for deployment
  - `README.md` - README file
  - `requirements.txt` - List of dependencies

## Contact
- If you have any questions, feel free to reach out to me at [strodenat@gmail.com](mailto:strodenat@gmail.com).
- [GitHub](https://github.com/strodenat)
