import uuid
from passlib.context import CryptContext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from app.models import UserModel, AdministrateurModel, RoleEnum

import bcrypt
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    db = SessionLocal()

    try:
        # Vérifier si l'admin existe déjà
        existing = db.query(UserModel).filter(
            UserModel.email == "admin@gmail.com"
        ).first()

        if existing:
            print("Admin déjà existant — seed ignoré.")
            return

        # Créer le User admin
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = UserModel(
            id          = str(uuid.uuid4()),
            nom         = "monteiro",
            prenom      = "dlm",
            email       = "admin@gmail.com",
            mot_de_pass = hashed_password,
            telephone   = None,
            role        = RoleEnum.ADMIN,
            photo       = "https://res.cloudinary.com/demo/image/upload/d31876a45d0482069e2c.png" 
        )
        db.add(admin_user)
        db.flush()

        # Créer l'Administrateur lié au User
        admin = AdministrateurModel(
            id      = str(uuid.uuid4()),
            user_id = admin_user.id
        )
        db.add(admin)
        db.commit()

        print("Admin créé avec succès !")
        print("Email    : admin@gmail.com")
        print("Password : admin123")

    except Exception as e:
        db.rollback()
        print(f"Erreur seed : {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()