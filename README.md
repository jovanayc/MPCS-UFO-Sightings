# MPCS-UFO-Sightings
May 28, 2025
MPCS Databases Final Project
By Alice Blander, Jovanay Carter, and Carter Harms

**Quick Way to View App**
- View online to see the database with: https://ufo-sightings-uchicago.streamlit.app/

**Project Intro**
The following is a simple, deployed streamlit web app for users to explore historical events and evidence related to UFO sightings in the U.S.

The primary focus of this project was database architecture, ER diagraming, data preprocessing, and data querying. Keep in mind, the frontend experince is purposefully simple due to the database focus of this project.

**UFO Database Details**
Our app connects to a MySQL database and draws from over 70,000 UFO sighting records to allow users to explore and ask questions about recent UFO sightings. We connect to a simple GUI for:

- Select from a list of supported queries
- Add filter parameters (like date ranges, states, or shapes)
- View query results in a clean table
- Insert a new UFO sighting record into the database

**Technology Used**
Frontend: Streamlit
Database: MySQL
Language: Python 3
Hosting: Streamlit Cloud
Source Control: GitHub

**How to Run the App Locally**
- Clone the Repo
- Install dependencies: pip install -r requirements.txt
- Create a file at .streamlit/secrets.toml with the folowing information:
    [mysql]
    host = "your-db-host"
    user = "your-db-username"
    password = "your-db-password"
    database = "ufo_db"
- Add the large data files called 'ufo-data' that you have stored locally to database/cleandata/[ufo-data]
- Run the app
    streamlit run UFO_App.py 

**How to Run and Inspect the MySQL Database Locally**
In order to check that the database is properly built and populated on your own machine, follow these steps.
- Start MySQL Server (if not already running):
    brew services start mysql
- Log Into MySQL
    mysql -u root -p
    Then senter your root password (same as in populated_database.py)
- List all available databases
    SHOW DATABASES;
- See UFO Database
    USE UFO;
- List All Tables
    SHOW TABLES;
    # TABLES SHOULD INCLUDE:
        | Article            |
        | EventKeywordTag    |
        | HistoricalEvent    |
        | KeywordsInEvent    |
        | KeywordsInSighting |
        | KeywordTag         |
        | Location           |
        | Sightings          |
        | UFO     
- View data in Tables
    SELECT * FROM Sighting LIMIT 10;
- Repeat for any other table you would like to verify
    SELECT * FROM UFO LIMIT 10;
    SELECT * FROM Keyword LIMIT 10;


