from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.produit_model import CategorieEnum, StatutPublicationEnum


# ============================================================
# PRODUIT SCHEMAS
# ============================================================

class ProduitCreate(BaseModel):
    nom            : str
    prix_unitaire  : float
    description    : Optional[str] = None
    quantite_stock : int
    photo          : Optional[str] = None
    categorie      : CategorieEnum
    agriculteur_id : str


class ProduitUpdate(BaseModel):
    nom            : Optional[str]           = None
    prix_unitaire  : Optional[float]         = None
    description    : Optional[str]           = None
    quantite_stock : Optional[int]           = None
    photo          : Optional[str]           = None
    categorie      : Optional[CategorieEnum] = None


class ProduitRead(BaseModel):
    id             : str
    nom            : Optional[str]
    prix_unitaire  : float
    description    : Optional[str]
    quantite_stock : int
    photo          : Optional[str]
    categorie      : CategorieEnum
    statut_publication : StatutPublicationEnum
    agriculteur_id : str
    date_creation  : datetime

    class Config:
        from_attributes = True