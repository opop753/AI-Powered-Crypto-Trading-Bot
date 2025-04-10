from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.model import Model
from backend.database import Base

DATABASE_URL = "sqlite:///./new_test.db"  # Ensure this matches the database used in init_db.py

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_sample_data():
    db = SessionLocal()
    try:
        # Create sample models
        sample_models = [
            Model(name="Model 1", enabled=True),
            Model(name="Model 2", enabled=True),
            Model(name="Model 3", enabled=False),
        ]
        db.add_all(sample_models)
        db.commit()
        print("Sample data added to the models table.")
    except Exception as e:
        print(f"Error adding sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
