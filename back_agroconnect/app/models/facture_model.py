import uuid
from datetime import date
from enum import Enum
from typing import Optional
from sqlalchemy import Column, String, Date, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class MoyenPaiementEnum(str, Enum):
    ORANGE_MONEY  = "orange_money"
    WAVE          = "wave"
    CARTE_BACAIRE = "carte_bacaire"


class FactureModel(Base):
    __tablename__ = "factures"

    id             = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date_facture   = Column(Date,   nullable=False, default=date.today)
    reference      = Column(String, nullable=True)
    moyen_paiement = Column(SAEnum(MoyenPaiementEnum), nullable=True)

    # Clé étrangère → Commande (multiplicité 1..1)
    commande_id = Column(String, ForeignKey("commandes.id"), nullable=False, unique=True)

    # Relations
    commande = relationship("CommandeModel", back_populates="facture")