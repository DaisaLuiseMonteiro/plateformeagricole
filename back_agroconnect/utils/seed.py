import uuid
from passlib.context import CryptContext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from app.models import UserModel, AdministrateurModel, AgriculteurModel, ClientModel, ProduitModel, RoleEnum
from app.models.produit_model import CategorieEnum, StatutPublicationEnum

import bcrypt
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed_all():
    db = SessionLocal()

    try:
        # ============================================================
        # 1. ADMIN
        # ============================================================
        existing_admin = db.query(UserModel).filter(UserModel.email == "admin@gmail.com").first()

        if existing_admin:
            print("⏩ Admin déjà existant — ignoré.")
        else:
            admin_user = UserModel(
                id          = str(uuid.uuid4()),
                nom         = "monteiro",
                prenom      = "dlm",
                email       = "admin@gmail.com",
                mot_de_pass = hash_password("admin123"),
                telephone   = "770000000",
                role        = RoleEnum.ADMIN,
                photo       = "https://res.cloudinary.com/demo/image/upload/d31876a45d0482069e2c.png"
            )
            db.add(admin_user)
            db.flush()

            admin = AdministrateurModel(id=str(uuid.uuid4()), user_id=admin_user.id)
            db.add(admin)
            db.flush()
            print(" Admin créé (admin@gmail.com / admin123)")

        # ============================================================
        # 2. AGRICULTEURS (4)
        # ============================================================
        agriculteurs_data = [
            {"nom": "Diallo",  "prenom": "Mamadou",  "email": "mamadou.diallo@agroconnect.comp",  "telephone": "775312222", "localisation": "Thiès, Sénégal"},
            {"nom": "Ndiaye",  "prenom": "Fatou",     "email": "fatou.ndiaye@agroconnect.com",    "telephone": "761234567", "localisation": "Saint-Louis, Sénégal"},
            {"nom": "Sow",     "prenom": "Ibrahima",  "email": "ibrahima.sow@agroconnect.com",    "telephone": "709876543", "localisation": "Ziguinchor, Sénégal"},
            {"nom": "Fall",    "prenom": "Aminata",   "email": "aminata.fall@agroconnect.com",    "telephone": "781112233", "localisation": "Kaolack, Sénégal"},
        ]

        agriculteur_ids = []

        for agri in agriculteurs_data:
            existing = db.query(UserModel).filter(UserModel.email == agri["email"]).first()
            if existing:
                print(f" Agriculteur {agri['email']} déjà existant — ignoré.")
                agri_record = db.query(AgriculteurModel).filter(AgriculteurModel.user_id == existing.id).first()
                if agri_record:
                    agriculteur_ids.append(agri_record.id)
                continue

            user = UserModel(
                id          = str(uuid.uuid4()),
                nom         = agri["nom"],
                prenom      = agri["prenom"],
                email       = agri["email"],
                mot_de_pass = hash_password("agri123"),
                telephone   = agri["telephone"],
                role        = RoleEnum.AGRICULTEUR,
                photo       = None
            )
            db.add(user)
            db.flush()

            agriculteur = AgriculteurModel(
                id           = str(uuid.uuid4()),
                user_id      = user.id,
                localisation = agri["localisation"],
                is_actif     = True
            )
            db.add(agriculteur)
            db.flush()

            agriculteur_ids.append(agriculteur.id)
            print(f"Agriculteur créé : {agri['prenom']} {agri['nom']} ({agri['email']} / agri123)")

        # ============================================================
        # 3. PRODUITS (12 = 3 par agriculteur)
        # ============================================================
        produits_data = [
            # Agriculteur 1 — Mamadou Diallo (Céréales)
            {
                "agriculteur_index": 0,
                "prix_unitaire": 1500,
                "description": "Un grain de qualité supérieure pour nourrir toute la famille ! Le riz carolina est riche en glucides et en vitamine B1.",
                "quantite_stock": 200,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576721/riz_carolina_vacuai.jpg",
                "categorie": CategorieEnum.CEREALE,
            },
            {
                "agriculteur_index": 0,
                "prix_unitaire": 800,
                "description": "Le mil, pilier de l'alimentation sénégalaise ! Riche en fer, en magnésium et en vitamine B6.",
                "quantite_stock": 300,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576561/grain_de_mil_zreufl.jpg",
                "categorie": CategorieEnum.CEREALE,
            },
            {
                "agriculteur_index": 0,
                "prix_unitaire": 1200,
                "description": "L'arachide sénégalaise, source d'énergie naturelle ! Contient de la vitamine E et des acides gras essentiels.",
                "quantite_stock": 250,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576324/arachide_jo6dxj.jpg",
                "categorie": CategorieEnum.CEREALE,
            },

            # Agriculteur 2 — Fatou Ndiaye (Fruits exotiques)
            {
                "agriculteur_index": 1,
                "prix_unitaire": 2500,
                "description": "Le kiwi, un concentré de vitalité pour vos journées ! Exceptionnellement riche en vitamine C et en vitamine K.",
                "quantite_stock": 80,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576534/kiwi_ub2sfg.jpg",
                "categorie": CategorieEnum.FRUIT,
            },
            {
                "agriculteur_index": 1,
                "prix_unitaire": 1800,
                "description": "La goyave, un trésor tropical au goût unique ! Riche en vitamine C, en vitamine A et en fibres.",
                "quantite_stock": 120,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576525/goyave_cca4l3.jpg",
                "categorie": CategorieEnum.FRUIT,
            },
            {
                "agriculteur_index": 1,
                "prix_unitaire": 3000,
                "description": "Le raisin, symbole de générosité et de douceur ! Riche en vitamine C, en vitamine K et en antioxydants.",
                "quantite_stock": 100,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576513/raisain_qkumlm.jpg",
                "categorie": CategorieEnum.FRUIT,
            },

            # Agriculteur 3 — Ibrahima Sow (Fruits & légumes)
            {
                "agriculteur_index": 2,
                "prix_unitaire": 2000,
                "description": "La datte, un fruit béni et énergisant ! Source naturelle de vitamine B6, de potassium et de magnésium.",
                "quantite_stock": 150,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576500/date_wljx8g.jpg",
                "categorie": CategorieEnum.FRUIT,
            },
            {
                "agriculteur_index": 2,
                "prix_unitaire": 500,
                "description": "La banane, l'allié sportif par excellence ! Riche en vitamine C, en vitamine B6 et en potassium.",
                "quantite_stock": 400,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576494/banane_ufabkw.jpg",
                "categorie": CategorieEnum.FRUIT,
            },
            {
                "agriculteur_index": 2,
                "prix_unitaire": 700,
                "description": "La carotte, pour une vue perçante et une peau radieuse ! Riche en vitamine A, en vitamine K et en bêta-carotène.",
                "quantite_stock": 300,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576463/carotte_pvtiwi.jpg",
                "categorie": CategorieEnum.LEGUME,
            },

            # Agriculteur 4 — Aminata Fall (Légumes)
            {
                "agriculteur_index": 3,
                "prix_unitaire": 600,
                "description": "La patate douce, un délice sucré et nutritif ! Riche en vitamine A, en vitamine C et en fibres.",
                "quantite_stock": 350,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576365/patate_n9sjiw.jpg",
                "categorie": CategorieEnum.LEGUME,
            },
            {
                "agriculteur_index": 3,
                "prix_unitaire": 900,
                "description": "Le gombo, incontournable dans la cuisine sénégalaise ! Riche en vitamine C, en vitamine K et en acide folique.",
                "quantite_stock": 200,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576363/gombo_b3gdrm.jpg",
                "categorie": CategorieEnum.LEGUME,
            },
            {
                "agriculteur_index": 3,
                "prix_unitaire": 750,
                "description": "L'aubergine, douce et polyvalente en cuisine ! Riche en vitamine B1, en vitamine B6 et en antioxydants.",
                "quantite_stock": 180,
                "photo": "https://res.cloudinary.com/dps0wgmoa/image/upload/q_auto/f_auto/v1776576359/aubergine_mjegec.jpg",
                "categorie": CategorieEnum.LEGUME,
            },
        ]

        for prod in produits_data:
            if prod["agriculteur_index"] >= len(agriculteur_ids):
                print(f" Agriculteur index {prod['agriculteur_index']} non disponible — produit ignoré.")
                continue

            produit = ProduitModel(
                id             = str(uuid.uuid4()),
                prix_unitaire  = prod["prix_unitaire"],
                description    = prod["description"],
                quantite_stock = prod["quantite_stock"],
                photo          = prod["photo"],
                categorie      = prod["categorie"],
                statut_publication = StatutPublicationEnum.PUBLIE,
                agriculteur_id = agriculteur_ids[prod["agriculteur_index"]]
            )
            db.add(produit)

        db.flush()
        print(" 12 produits créés avec succès !")

        # ============================================================
        # 4. CLIENTS (5)
        # ============================================================
        clients_data = [
            {"nom": "Ba",      "prenom": "Ousmane",   "email": "ousmane.ba@gmail.com",     "telephone": "771112233", "adresse": "Dakar, Médina"},
            {"nom": "Sarr",    "prenom": "Aissatou",  "email": "aissatou.sarr@gmail.com",  "telephone": "762223344", "adresse": "Dakar, Parcelles Assainies"},
            {"nom": "Gueye",   "prenom": "Moussa",    "email": "moussa.gueye@gmail.com",   "telephone": "703334455", "adresse": "Rufisque, Sénégal"},
            {"nom": "Diouf",   "prenom": "Mariama",   "email": "mariama.diouf@gmail.com",  "telephone": "784445566", "adresse": "Mbour, Sénégal"},
            {"nom": "Camara",  "prenom": "Lamine",    "email": "lamine.camara@gmail.com",  "telephone": "755556677", "adresse": "Tambacounda, Sénégal"},
        ]

        for cl in clients_data:
            existing = db.query(UserModel).filter(UserModel.email == cl["email"]).first()
            if existing:
                print(f" Client {cl['email']} déjà existant — ignoré.")
                continue

            user = UserModel(
                id          = str(uuid.uuid4()),
                nom         = cl["nom"],
                prenom      = cl["prenom"],
                email       = cl["email"],
                mot_de_pass = hash_password("client123"),
                telephone   = cl["telephone"],
                role        = RoleEnum.CLIENT,
                photo       = None
            )
            db.add(user)
            db.flush()

            client = ClientModel(
                id      = str(uuid.uuid4()),
                user_id = user.id,
                adresse = cl["adresse"]
            )
            db.add(client)
            db.flush()
            print(f" Client créé : {cl['prenom']} {cl['nom']} ({cl['email']} / client123)")

        # ============================================================
        # COMMIT FINAL
        # ============================================================
        db.commit()
        print("\n🎉 Seed terminé avec succès !")
        print("=" * 50)
        print("Admin       : admin@gmail.com / admin123")
        print("Agriculteurs: *@agroconnect.sn / agri123")
        print("Clients     : *@gmail.com / client123")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f" Erreur seed : {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    seed_all()