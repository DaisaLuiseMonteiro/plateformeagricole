from pydantic import BaseModel
from typing import Optional
from datetime import date
from facture_models import MoyenPaiementEnum


# ============================================================
# FACTURE SCHEMAS
# ============================================================

class FactureCreate(BaseModel):
    reference      : Optional[str]              = None
    moyen_paiement : Optional[MoyenPaiementEnum] = None
    commande_id    : str


class FactureUpdate(BaseModel):
    reference      : Optional[str]              = None
    moyen_paiement : Optional[MoyenPaiementEnum] = None


class FactureRead(BaseModel):
    id             : str
    date_facture   : date
    reference      : Optional[str]
    moyen_paiement : Optional[MoyenPaiementEnum]
    commande_id    : str

    class Config:
        from_attributes = True