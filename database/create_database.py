import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join("..", ".env"))
load_dotenv(".env") # fallback

def create_database():
    """Connects to default postgres database to create the target database."""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    dbname = os.environ.get("POSTGRES_DB", "sales_intelligence")

    try:
        # Connect to the default 'postgres' database first
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cur.fetchone()

        if not exists:
            print(f"Creating database: {dbname}")
            cur.execute(f"CREATE DATABASE {dbname}")
        else:
            print(f"Database {dbname} already exists.")

        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def initialize_schema():
    """Connects to the newly created database and executes schema.sql"""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    dbname = os.environ.get("POSTGRES_DB", "sales_intelligence")

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        cur = conn.cursor()
        
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        print(f"Executing schema from {schema_path}...")
        
        with open(schema_path, "r") as f:
            schema_sql = f.read()
            
        cur.execute(schema_sql)
        conn.commit()
        
        cur.close()
        conn.close()
        print("Schema initialized successfully.")
        
    except Exception as e:
        print(f"Error initializing schema: {e}")

if __name__ == "__main__":
    print("--- Setting up PostgreSQL Database ---")
    if create_database():
        initialize_schema()
