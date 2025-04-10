from sqlalchemy import create_engine
from backend.database import Base
from backend.models.model import Model

DATABASE_URL = "sqlite:///./new_test.db"  # Updated to use a new database file

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create the tables in the database
import os  # Import os module to check for file existence

def database_exists(db_url):
    return os.path.exists(db_url.split("///")[-1])  # Extract the database file path

def init_db():
    if not database_exists(DATABASE_URL):
        Base.metadata.create_all(bind=engine)
    else:
        logging.info("Database already exists. No need to create tables.")

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")
