import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Float, Integer, Enum as SAEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class CategorieEnum(str, Enum):
    LEGUME  = "legume"
    CEREALE = "cereale"
    FRUIT   = "fruit"

class StatutPublicationEnum(str, Enum):
    EN_ATTENTE = "en_attente"
    PUBLIE     = "publie"
    REJETE     = "rejete"


class ProduitModel(Base):
    __tablename__ = "produits"

    id             = Column(String,  primary_key=True, default=lambda: str(uuid.uuid4()))
    prix_unitaire  = Column(Float,   nullable=False)
    description    = Column(String,  nullable=True)
    quantite_stock = Column(Integer, nullable=False, default=0)
    photo          = Column(String,  nullable=True)
    categorie      = Column(SAEnum(CategorieEnum), nullable=False)
    statut_publication = Column(SAEnum(StatutPublicationEnum), nullable=False, default=StatutPublicationEnum.EN_ATTENTE)
    date_creation  = Column(DateTime, default=datetime.utcnow)

    # Clé étrangère → Agriculteur
    agriculteur_id = Column(String, ForeignKey("agriculteurs.id"), nullable=False)

    # Relations
    agriculteur = relationship("AgriculteurModel", back_populates="produits")
    details     = relationship("DetailsModel",     back_populates="produit")