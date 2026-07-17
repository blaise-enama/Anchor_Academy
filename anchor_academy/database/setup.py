import pymysql
import os
import logging
from pymysql import MySQLError
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

def connect_to_database():

    """
    Establishes a connection to the MySQL database using credentials from environment variables.
    Returns the connection object if successful, or None if there was an error.
    """

    try:
        # Load database credentials from environment variables
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'Anchor_Academy')

        # Connect to the database
        connection = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
        logging.info("Successfully connected to the database.")
        return connection


    except Exception as e   :
        logging.error(f"Error connecting to the database: {e}")
        return None


def initialize_anchor_academy():
    """
    Using input(), prompt the user to enter additional details (ie: database connection)
    *if user has an existing database, prompt for credentials and connect to it
    *if user does not have an existing database, prompt to create a new one with default Anchor Academy credentials (localhost, root, password, Anchor_Academy)
    *if user does not have mysql installed, prompt to install mysql and create a database with
    """
    """
    print("Before starting, please ensure that you have MySQL installed and running.")
    print("We're going to need some information in order to connect to your database.")
    """

    #prompt the user for database connection details... maybe in a while loop until they provide valid credentials or choose to create a new database
    logging.info(f"Database connection triggered.") 
    database = input("Do you have an existing MySQL database for Anchor Academy? (yes/no): ").strip().lower()
    if database == "yes":
        db_host = input("Enter your database host (default: localhost): ") or "localhost"
        db_port = input("Enter your database port (default: 3306): ") or "3306"
        db_name = input("Enter your database name (default: Anchor_Academy): ") or "Anchor_Academy"
        db_user = input("Enter your database username (default: root): ") or "root"
        db_password = input("Enter your database password (default: empty): ") or ""   
    
    elif database == "no":
        print("One moment as we set up a new Anchor Academy database for you...")
    
        try:
            # Connect to MySQL server
            conn = pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'Anchor_Academy'),
                cursorclass=pymysql.cursors.DictCursor
            )

    #create a database
            with conn.cursor() as cursor:
                cursor.execute(
                    "CREATE DATABASE IF NOT EXISTS Anchor_Academy"
                )
            conn.commit()

            print("Connecting to MySQL Server...")
            print("Creating 'Anchor_Academy' database...")
            print("Database 'Anchor_Academy' created successfully!")


            conn.close()
            
            #maybe explain the schema and tables that will be created in the database for the user to understand what is being set up
            print("\n The following schema and tables will be created in the 'Anchor_Academy' database:")
            print(" - roster (Players' table) : Stores player information such as name, age, position, etc.")
            print(" - Sessions table: Records training session details including date, duration, and performance metrics.")
            print(" - PerformanceMetrics table: Holds detailed performance data for each player.")

        except MySQLError as e:
            print(f"Error connecting to MySQL server: {e}")
            return
        
        connection = connect_to_database()

        if connection:
            print("\nSetup complete. You may now begin ingesting player data.")

            #connection.close()

    else:
        print(" Unable to connect to the Anchor_Academy database")


if __name__ == "__main__":
    initialize_anchor_academy()
    