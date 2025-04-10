from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.model import Model

def add_models(db: Session):
    models_to_add = [
        {"name": "XGBoost", "enabled": True},
        {"name": "Random Forest", "enabled": True},
        {"name": "RNN LSTM", "enabled": True},
        {"name": "CNN", "enabled": True},
        {"name": "LSTM", "enabled": True},
    ]
    
    for model_data in models_to_add:
        model = db.query(Model).filter(Model.name == model_data["name"]).first()
        if not model:
            new_model = Model(**model_data)
            db.add(new_model)
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        add_models(db)
    finally:
        db.close()
