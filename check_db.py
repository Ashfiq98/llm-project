import psycopg2
from psycopg2 import OperationalError

def check_connection():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="mydb",               # Database name
            user="user",                 # Database user
            password="password",         # Database password
            host="scrapy-project-db-1",  # Database host (container name)
            port="5432"                  # Database port
        )

        # If connection is successful
        print("Database connection successful.")
        connection.close()  # Close the connection after use

    except OperationalError as e:
        # If there's an error connecting to the database
        print(f"Error: {e}")

if __name__ == "__main__":
    check_connection()
