import os
import uuid
import csv
from flask import Flask, g
from dotenv import load_dotenv
import utils.db as DBUtils

# Load environment variables from .env file
load_dotenv()

# Create an instance of the Flask application
app = Flask(__name__)

# Add configuration data to your application
app.config["DATABASE"] = os.getenv("DATABASE")
app.config["DBHOST"] = os.getenv("DBHOST")
app.config["DBUSERNAME"] = os.getenv("DBUSERNAME")
app.config["DBPASSWORD"] = os.getenv("DBPASSWORD")

# Debug print statements to verify that environment variables are loaded
print("Database:", app.config["DATABASE"])
print("Host:", app.config["DBHOST"])
print("Username:", app.config["DBUSERNAME"])
print("Password:", app.config["DBPASSWORD"])

# Useful if you decide to create session cookies
app.config["SECRET_KEY"] = uuid.uuid4().hex

# Setup Views
# Ensure these blueprints exist and are correctly implemented
try:
    from views.task_view import task_list_blueprint
    from api.task_api import task_api_blueprint
    app.register_blueprint(task_list_blueprint)
    app.register_blueprint(task_api_blueprint)
except ImportError as e:
    print(f"Import error: {e}")

# Helper function to establish a connection to the database
def connect_db():
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = DBUtils.connect_db(app.config)
    if not hasattr(g, 'mysql_cursor'):
        g.mysql_cursor = g.mysql_db.cursor(dictionary=True)

# Helper function to release the connection to the database
def disconnect_db():
    if hasattr(g, 'mysql_cursor'):
        g.mysql_cursor.close()
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()

# Command to initialize the database
@app.cli.command('initdb')
def initdb_cli_command():
    try:
        DBUtils.init_db(app.config, "app/book_data.csv", "app/customer_data.csv")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Function called before all requests
@app.before_request
def before():
    connect_db()

# Function called after all requests
@app.after_request
def after(response):
    disconnect_db()
    return response

print("Loading environment variables...")
load_dotenv()


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
