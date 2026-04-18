from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.models.commande_model import StatutEnum


# ============================================================
# DETAILS SCHEMAS
# ============================================================

class ItemCreate(BaseModel):
    produit_id: str
    quantite: int
    montant: float

class DetailsCreate(BaseModel):
    quantite    : int
    montant     : float
    commande_id : str
    produit_id  : str


class DetailsUpdate(BaseModel):
    quantite : Optional[int]   = None
    montant  : Optional[float] = None


class DetailsRead(BaseModel):
    id          : str
    quantite    : int
    montant     : float
    commande_id : str
    produit_id  : str
    agriculteur_nom: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================
# COMMANDE SCHEMAS
# ============================================================

class CommandeCreate(BaseModel):
    client_id : str
    montant_total: float
    items: List[ItemCreate]


class CommandeUpdate(BaseModel):
    statut           : Optional[StatutEnum] = None
    montant_commande : Optional[float]      = None


class CommandeRead(BaseModel):
    id               : str
    date_commande    : date
    statut           : StatutEnum
    montant_commande : float
    client_id        : str
    details          : Optional[List[DetailsRead]] = []

    class Config:
        from_attributes = True