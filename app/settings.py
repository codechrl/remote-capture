import os

from dotenv import load_dotenv

# Define the path to the project root directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the .env file from the root directory
dotenv_path = os.path.join(project_dir, ".env")
load_dotenv(dotenv_path)

# Access the environment variables
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
HOSTNAME = str(os.getenv("HOSTNAME"))
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
