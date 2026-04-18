import uuid
from datetime import date
from enum import Enum
from sqlalchemy import Column, String, Float, Integer, Date, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class StatutEnum(str, Enum):
    EN_ATTENTE = "En_attente"
    VALIDEE    = "validée"
    ANNULEE    = "annulée"
    LIVREE     = "livrée"
    CONFIRMEE  = "confirmée"


class CommandeModel(Base):
    __tablename__ = "commandes"

    id               = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date_commande    = Column(Date,   nullable=False, default=date.today)
    statut           = Column(SAEnum(StatutEnum), nullable=False, default=StatutEnum.EN_ATTENTE)
    montant_commande = Column(Float,  nullable=False, default=0.0)

    # Clé étrangère → Client
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)

    # Relations
    client  = relationship("ClientModel",  back_populates="commandes")
    details = relationship("DetailsModel", back_populates="commande")
    facture = relationship("FactureModel", back_populates="commande", uselist=False)


class DetailsModel(Base):
    __tablename__ = "details"

    id       = Column(String,  primary_key=True, default=lambda: str(uuid.uuid4()))
    quantite = Column(Integer, nullable=False)
    montant  = Column(Float,   nullable=False)

    # Clé étrangère → Commande
    commande_id = Column(String, ForeignKey("commandes.id"), nullable=False)

    # Clé étrangère → Produit
    produit_id  = Column(String, ForeignKey("produits.id"),  nullable=False)

    # Relations
    commande = relationship("CommandeModel", back_populates="details")
    produit  = relationship("ProduitModel",  back_populates="details")

    @property
    def agriculteur_nom(self):
        if self.produit and self.produit.agriculteur and self.produit.agriculteur.user:
            user = self.produit.agriculteur.user
            return f"{user.prenom} {user.nom}"
        return "Inconnu"