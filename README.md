# Solvent Selector

This is a flask CRUD web app that lets the user see different solvents using different reactions. Flask will make the web app, rdkit will make the molecular structure of the solvents, SQLite/SQLalchemy will store different reactions and solvents in a database, and HTML/CSS will be used for styling. I started this project as I recently finished learning about databases in my course and also saw an internship that piqued my interest in combining CS and chemistry into cheminformatics so I made a small web app as a small proof of concept just to see if I am capable of doing an internship as a first year.
## Prerequisites

- Python 3.x
- pip (Python package installer)

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/Ahmed-Nadeem-Malik/Solvent-Selector.git
    cd solvent-selector
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

5. Initialize the database:

    ```sh
    flask db upgrade
    ```

6. Run the application:

    ```sh
    flask run
    ```

7. Open your web browser and go to `http://127.0.0.1:5000` to view the application.
