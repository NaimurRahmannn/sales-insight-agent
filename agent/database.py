import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from . import config

def get_db_connection():
    """
    Creates and tests a connection to the PostgreSQL analytics database.
    Returns a SQLAlchemy Engine object.
    """
    connection_string = f"postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    
    try:
        engine = create_engine(connection_string, pool_pre_ping=True)
        # Test connection
        with engine.connect() as conn:
            pass
        return engine
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e

# Create a global engine instance for tools to use
engine = get_db_connection()
