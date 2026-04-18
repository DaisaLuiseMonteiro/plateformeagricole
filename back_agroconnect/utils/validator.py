from sqlalchemy.orm import Session
from models.user_model import User

def email_exists(db: Session, email: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    return user is not None

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()