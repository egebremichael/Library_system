# Imports for built-in Python libraries
import os
import uuid
import csv
import logging  # For error logging

# Imports for 3rd-party libraries
from flask import Flask, g
from dotenv import load_dotenv

# Imports for blueprints and other modules
import utils.db as DBUtils 
from flask import render_template


# Load environment variables from .env file if available
load_dotenv()

# Create Flask app instance
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

# Set up app configurations for database connection
app.config["DATABASE"] = os.getenv("DATABASE", "library_db")
app.config["DBHOST"] = os.getenv("DBHOST", "localhost")
app.config["DBUSERNAME"] = os.getenv("DBUSERNAME", "root")
app.config["DBPASSWORD"] = os.getenv("DBPASSWORD", "")

# Secret key for session management (if required)
app.config["SECRET_KEY"] = uuid.uuid4().hex

# Setup logging to track errors
logging.basicConfig(level=logging.DEBUG)

# Helper function to establish a connection to the database
def connect_db():
    try:
        if not hasattr(g, 'mysql_db'):
            g.mysql_db = DBUtils.connect_db(app.config)  # Connecting to the DB
        if not hasattr(g, 'mysql_cursor'):
            g.mysql_cursor = g.mysql_db.cursor(
                dictionary=True)  # Cursor for queries
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")

# Helper function to release the connection to the database
def disconnect_db():
    try:
        if hasattr(g, 'mysql_cursor'):
            g.mysql_cursor.close()
        if hasattr(g, 'mysql_db'):
            g.mysql_db.close()
    except Exception as e:
        logging.error(f"Error disconnecting from database: {e}")

# Custom Flask CLI command to initialize the database
@app.cli.command('initdb')
def initdb_cli_command():
    try:
        DBUtils.init_db(app.config, "app/book_data.csv",
                        "app/customer_data.csv")
        print("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")

# Function called before each request to the webservice
@app.before_request
def before_request():
    connect_db()

# Function called after each webservice request
@app.after_request
def after_request(response):
    disconnect_db()
    return response

# Run the Flask app
if __name__ == "__main__":
     app.run(debug=True, host="0.0.0.0", port=3000)
