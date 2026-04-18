import uuid
from datetime import datetime, date
from enum import Enum
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from database import Base

class StatutProductionEnum(str, Enum):
    EN_ATTENTE = "en_attente"
    RELANCEE   = "relancee"
    ACCEPTEE   = "acceptee"
    REJETEE    = "rejetee"

class DemandeProductionModel(Base):
    __tablename__ = "demandes_production"

    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nom_produit  = Column(String, nullable=False)
    quantite     = Column(Integer, nullable=False)
    description  = Column(String, nullable=True)
    date_limite  = Column(Date, nullable=True) # Deadline set by Admin
    statut       = Column(SAEnum(StatutProductionEnum), default=StatutProductionEnum.EN_ATTENTE)
    date_creation = Column(DateTime, default=datetime.utcnow)

    # Clé étrangère → Client
    client_id    = Column(String, ForeignKey("clients.id"), nullable=False)
    
    # Clé étrangère → Agriculteur (celui qui a accepté)
    agriculteur_accepte_id = Column(String, ForeignKey("agriculteurs.id"), nullable=True)

    # Relations
    client    = relationship("ClientModel")
    agriculteur = relationship("AgriculteurModel")
    relances  = relationship("RelanceProductionModel", back_populates="demande")


class RelanceProductionModel(Base):
    __tablename__ = "relances_production"

    id             = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    demande_id     = Column(String, ForeignKey("demandes_production.id"), nullable=False)
    agriculteur_id = Column(String, ForeignKey("agriculteurs.id"), nullable=False)
    statut         = Column(String, default="en_attente") # en_attente, accepte, rejete

    # Relations
    demande     = relationship("DemandeProductionModel", back_populates="relances")
    agriculteur = relationship("AgriculteurModel")
