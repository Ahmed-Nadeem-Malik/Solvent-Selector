# Solvent Selector

This is a flask CRUD web app that lets the user see different solvents using different reactions. Flask will make the web app, rdkit will make the molecular structure of the solvents, SQLite/SQLalchemy will store different reactions and solvents in a database, and HTML/CSS will be used for styling. I started this project as I recently finished learning about databases in my course and also saw an internship that piqued my interest in combining CS and chemistry into cheminformatics so I made a small web app as a small proof of concept just to see if I am capable of doing an internship as a first year.
# Prerequisites

1. **Python 3.x** – Make sure you have Python installed.
2. **pip** – Python’s package installer.
3. *(Optional but recommended)* **Virtual Environment Tool** – For example, using Python’s built‑in `venv`.
4. **RDKit** – This project uses RDKit to render molecular structures. Because RDKit is not available via pip on every platform, it is recommended to install it via conda (see note below).

---
Setup and Running Instructions

1. Clone the Repository

Open your terminal and clone the repository:

git clone https://github.com/Ahmed-Nadeem-Malik/Solvent-Selector.git
cd Solvent-Selector

2. Create a Virtual Environment

Create a new virtual environment:

python3 -m venv venv

Then activate it:

On macOS/Linux:

source venv/bin/activate

On Windows:

venv\Scripts\activate

3. Install Dependencies

Install all required Python packages:

pip install -r requirements.txt

Note: If you need RDKit and it is not installed via pip on your platform, it is recommended to use Conda. For example:

conda create -n solvent_selector python=3.x rdkit -c rdkit
conda activate solvent_selector
pip install -r requirements.txt

4. Set Up the Database

This project uses SQLite with SQLAlchemy and Flask-Migrate. Initialize (or upgrade) your database by running:

flask db upgrade

(If you haven’t set any migration directory before, you might need to initialize it first with flask db init—however, the repository already contains a migrations folder.)

5. Set Environment Variables (Optional)

To use Flask’s CLI for running the app, set the following environment variables:

On macOS/Linux:

export FLASK_APP=app.py
export FLASK_ENV=development

On Windows (cmd):

set FLASK_APP=app.py
set FLASK_ENV=development

6. Run the Application

You have two options:

Option A: Using the Flask CLI

flask run

Option B: Running the App Directly

python app.py

7. Access the Web App

Open your web browser and navigate to:

http://127.0.0.1:5000/


Please let me know if you have any recommendations to make this better, I just want to improve as a programmer :)
