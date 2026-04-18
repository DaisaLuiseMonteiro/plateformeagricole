from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class DemandeProductionCreate(BaseModel):
    nom_produit: str
    quantite: int
    description: Optional[str] = None
    client_id: str

class DemandeProductionRead(BaseModel):
    id: str
    nom_produit: str
    quantite: int
    description: Optional[str]
    date_limite: Optional[date]
    statut: str
    date_creation: datetime
    client_id: str
    agriculteur_accepte_id: Optional[str]

    class Config:
        from_attributes = True

class DemandeRelance(BaseModel):
    demande_id: str
    agriculteur_ids: List[str]
    date_limite: date
