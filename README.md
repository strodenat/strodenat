Portfolio Website with Python Game
This is my portfolio website showcasing my projects and skills. The website includes a Python game that is hosted using Flask.

Table of Contents
About
Features
Technologies Used
Installation
Usage
Folder Structure
License
Contact
About
This portfolio website is designed to showcase my projects, skills, and experiences. It includes a section where visitors can play a Python game that I developed. The game is hosted using Flask, a lightweight WSGI web application framework.

Features
Home page with an introduction and overview of my skills.
Projects page displaying various projects I've worked on.
Game section where visitors can play a Python game.
Contact form for visitors to reach out to me.
Technologies Used
HTML, CSS, JavaScript for the front-end.
Flask for the back-end.
Python for the game logic.
Deployed using a suitable web server.
Installation
<br>
Clone the repository:
<br>
In bash:
<br>
git clone https://github.com/yourusername/portfolio-website.git
<br>
cd portfolio-website
<br>
Create a virtual environment and activate it:
<br>
python3 -m venv venv
<br>
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
<br>
Install the required dependencies:
<br>
pip install -r requirements.txt
<br>
Set the Flask app environment variable:
<br>
<br>
export FLASK_APP=app.py  # On Windows, use `set FLASK_APP=app.py`
<br>
Run the Flask application:
<br>
<br>
flask run
<br>
Open your browser and go to http://127.0.0.1:5000 to view the website.
<br>
Usage
<br>
Navigate through the various sections to learn more about my skills and projects.
<br>
Play the Python game hosted on the site by visiting the game section.
<br>
Use the contact form to get in touch with me.
<br>
Folder Structure
<br>
csharp
<br>
Copy code
<br>
portfolio-website/
│
├── __pycache__/         # Cache files
├── game/                # Python game files
├── static/              # Static files (CSS, JavaScript, images)
├── templates/           # HTML templates
├── app.py               # Flask application file
├── Procfile             # Procfile for deployment
├── README.md            # README file
└── requirements.txt     # List of dependencies
