import pymysql
import os
import getpass
import logging

from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
from typing import Optional, Tuple
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()


def prompt_for_db_credentials() -> Tuple[str, int, str, str, str]:
    """
    Ask the user for DB connection details.
    Returns: host, port, db_name, user, password
    """
    host = input(f"DB host (default: {os.getenv('DB_HOST', 'localhost')}): ").strip() or os.getenv("DB_HOST", "localhost")
    port_raw = input(f"DB port (default: {os.getenv('DB_PORT', '3306')}): ").strip() or os.getenv("DB_PORT", "3306")
    try:
        port = int(port_raw)
    except ValueError:
        logging.warning("Invalid port entered; using 3306.")
        port = 3306
    
    db_name = input(f"Database name (default: {os.getenv('DB_NAME', 'Anchor_Academy')}): ").strip() or os.getenv("DB_NAME", "Anchor_Academy")
    user = input(f"DB user (default: {os.getenv('DB_USER', 'root')}): ").strip() or os.getenv("DB_USER", "root")
    password = getpass.getpass("DB password (leave blank for none): ") or os.getenv("DB_PASSWORD", "")
    
    return host, port, db_name, user, password


def try_connect(host: str, port, user: str, password: str, database: Optional[str] = None):
    """Attempt a pymysql connection and return it or raise."""
    
    # Ensure port is an int
    try:
        port_int = int(port)

    except (TypeError, ValueError):
        logging.warning("Invalid port provided; falling back to 3306")
        port_int = 3306

    conn_kwargs = dict(host=host, user=user, password=password, port=port_int, cursorclass=DictCursor)
    if database:
        conn_kwargs["database"] = database
    
    return pymysql.connect(**conn_kwargs)


def create_database_if_missing(host: str, port: int, user: str, password: str, db_name: str) -> bool:
    """Connect to server and create the database if it doesn't exist."""
    try:
        logging.info("Connecting to MySQL server to ensure database exists... Please wait one moment.")
        conn = try_connect(host, port, user, password)
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        conn.commit()
        conn.close()
        logging.info(f"Database '{db_name}' ensured.")
        return True
    except MySQLError as e:
        logging.info(f"Creating missing database...")
        logging.error(f"Error creating database: {e}")
        return False


def connect_to_database(interactive: bool = False) -> Optional[pymysql.connections.Connection]:

    """
    Establishes a connection to the MySQL database using credentials from environment variables.
    Returns the connection object connected to the Anchor_Academy database, or None. 
    if successful, or None if there was an error.
    """

    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "Anchor_Academy")

    if interactive:
        """
        Executes when user opts to run demo mode with in-memory data
        (prompts the user for mysql database credentials) 
        """
        while True:
            print("\n--- Database connection setup ---")
            #host, port, db_name, user, password = prompt_for_db_credentials()

            try:
                #connect to the database using the above credentials
                conn = try_connect(host, port, user, password, database=db_name)
                logging.info("Connected to database successfully.")
                logging.info("interactive connection passed.")
                return conn
            
            except MySQLError as e:
                logging.error(f"Connection failed: {e}")
                choice = input("Retry credentials? (yes/no): ").strip().lower()
                if choice != "yes":
                    logging.info("Aborting interactive DB connection.")
                    return None
    else:
        #interactive = False
        try:
            conn = try_connect(host, port, user, password, database=db_name)
            logging.info("Connected to DB (non-interactive) successfully.")
            return conn
        except MySQLError as e:
            logging.error(f"Non-interactive connection failed: {e}")
            return None




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
        
    """


def initialize_anchor_academy(host: Optional[str]= None, port: Optional[int] = None, user: Optional[str] = None, password:Optional[str] = None, db_name: Optional[str] = None) -> bool:
    """
    Initializes the Anchor_Academy database and creates required tables. Returns True on success.

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
    logging.info(f"initialize_anchor_academy called.")
    logging.info(f"Database connection triggered. Beginning Database initialization.") 

    host= host or os.getenv("DB_HOST", "localhost")
    port= port or os.getenv("DB_PORT", 3306)
    user= user or os.getenv("DB_USER", "root")
    db_name= db_name or os.getenv("DB_NAME", "Anchor_Academy")
    password= password if password is not None else os.getenv("DB_PASSWORD")

    if not create_database_if_missing(host, port, user, password, db_name):
        return False
    
    try:
        conn = try_connect(host,port, user, password, database=db_name)
        with conn.cursor() as curs:
            #create player/ roster tables/schemas for new mysql connections
            #since the credentials I'm using/ testing with already follow this schema, a new one can't be created
            curs.execute(
                """
                CREATE TABLE IF NOT EXISTS roster (
                    player_id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(50) NOT NULL, 
                    position VARCHAR(64),
                    age INT,
                    team VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB;
                """
            )

            #sessions table
            curs.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INT AUTO_INCREMENT PRIMARY KEY,
                    player_id INT NOT NULL,
                    session_date DATE,
                    duration_minutes INT,
                    sprint_count INT,
                    total_distance FLOAT,
                    max_speed FLOAT,
                    touches_left INT DEFAULT 0,
                    touches_right INT DEFAULT 0,
                    FOREIGN KEY (player_id) REFERENCES roster(player_id) ON DELETE CASCADE
                ) ENGINE=InnoDB;
                """
            )

            # performance metrics table (key-value style)
            curs.execute(
                """
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    metric_id INT AUTO_INCREMENT PRIMARY KEY,
                    session_id INT NOT NULL,
                    metric_name VARCHAR(128) NOT NULL,
                    metric_value DOUBLE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                ) ENGINE=InnoDB;
                """
            )
        conn.commit()
        conn.close()
        logging.info("Anchor_Academy schema initialized successfully.")
        return True
    
    except MySQLError as e:
        logging.error(f"Error initializing schema: {e}")
        return False

    """database = input("Do you have an existing MySQL database for Anchor Academy? (yes/no): ").strip().lower()
    if database == "yes":
        db_host = input("Enter your database host (default: localhost): ") or "localhost"
        db_port = input("Enter your database port (default: 3306): ") or "3306"
        db_name = input("Enter your database name (default: Anchor_Academy): ") or "Anchor_Academy"
        db_user = input("Enter your database username (default: root): ") or "root"
        db_password = input("Enter your database password (default: empty): ") or ""  

        conn=pymysql.connect(
            host= db_host,
            user= db_user,
            password= db_password,
            database=db_name,
            port= db_port
        ) 
    
    elif database == "no":
        print("One moment as we set up a new Anchor Academy database for you...")
    
        try:
            # Connect to MySQL server
            conn = pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password= password if password is not None else os.getenv('DB_PASSWORD', ''),
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
        
"""


if __name__ == "__main__":
    if __name__ == "__main__":
    # Quick manual run helper used during development:
        print("This script will ensure the Anchor_Academy database and tables exist.")
        use_interactive = input("Run interactively to enter credentials? (yes/no): ").strip().lower() == "yes"
        if use_interactive:
            conn = connect_to_database(interactive=True)
            if conn:
                print("Connection succeeded.")
                conn.close()
        else:
            ok = initialize_anchor_academy()
            print("Initialization", "succeeded" if ok else "failed")