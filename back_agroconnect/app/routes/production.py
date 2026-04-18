from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database import get_db
from app.models.production_model import DemandeProductionModel, RelanceProductionModel, StatutProductionEnum
from app.models.notification_model import NotificationModel
from app.models.user_model import UserModel, RoleEnum, AgriculteurModel
from app.schemas.production_schema import DemandeProductionCreate, DemandeProductionRead, DemandeRelance
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/production",
    tags=["Production sur Commande"]
)

@router.post("/demande", response_model=DemandeProductionRead, status_code=status.HTTP_201_CREATED)
def creer_demande_production(demande_data: DemandeProductionCreate, db: Session = Depends(get_db)):
    # 1. Création de la demande
    nouvelle_demande = DemandeProductionModel(
        nom_produit=demande_data.nom_produit,
        quantite=demande_data.quantite,
        description=demande_data.description,
        client_id=demande_data.client_id,
        statut=StatutProductionEnum.EN_ATTENTE
    )
    db.add(nouvelle_demande)
    db.commit()
    db.refresh(nouvelle_demande)

    # 2. Notification pour l'administrateur
    admin = db.query(UserModel).filter(UserModel.role == RoleEnum.ADMIN).first()
    if admin:
        nouvelle_notif = NotificationModel(
            user_id=admin.id,
            titre="Nouvelle demande de production",
            message=f"Un client demande la production de {nouvelle_demande.quantite} {nouvelle_demande.nom_produit}.",
            type="action_required",
            data=json.dumps({"demande_id": nouvelle_demande.id, "type": "production_request"})
        )
        db.add(nouvelle_notif)
        db.commit()

    return nouvelle_demande

@router.post("/relance")
def relancer_demande(relance_data: DemandeRelance, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Réservé à l'admin")

    demande = db.query(DemandeProductionModel).filter(DemandeProductionModel.id == relance_data.demande_id).first()
    if not demande:
        raise HTTPException(status_code=404, detail="Demande introuvable")

    # Mettre à jour la demande
    demande.statut = StatutProductionEnum.RELANCEE
    demande.date_limite = relance_data.date_limite

    # Créer les relances pour chaque agriculteur
    for agr_id in relance_data.agriculteur_ids:
        # Vérifier si l'agriculteur existe
        agriculteur = db.query(AgriculteurModel).filter(AgriculteurModel.id == agr_id).first()
        if not agriculteur: continue

        relance = RelanceProductionModel(
            demande_id=demande.id,
            agriculteur_id=agr_id,
            statut="en_attente"
        )
        db.add(relance)
        db.flush()

        # Notifier l'agriculteur
        nouvelle_notif = NotificationModel(
            user_id=agriculteur.user_id,
            titre="Opportunité de production",
            message=f"L'admin vous propose de produire {demande.quantite} {demande.nom_produit} avant le {demande.date_limite}.",
            type="action_required",
            data=json.dumps({"relance_id": relance.id, "type": "production_opportunity"})
        )
        db.add(nouvelle_notif)

    db.commit()
    return {"message": "Demande relancée auprès des agriculteurs sélectionnés."}

@router.post("/accepter/{relance_id}")
def accepter_production(relance_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    relance = db.query(RelanceProductionModel).filter(RelanceProductionModel.id == relance_id).first()
    if not relance:
        raise HTTPException(status_code=404, detail="Relance introuvable")

    demande = relance.demande
    if demande.statut == StatutProductionEnum.ACCEPTEE:
        raise HTTPException(status_code=400, detail="Cette commande a déjà été acceptée par un autre agriculteur")

    # 1. Mettre à jour la relance et la demande
    relance.statut = "accepte"
    demande.statut = StatutProductionEnum.ACCEPTEE
    demande.agriculteur_accepte_id = relance.agriculteur_id

    # 2. Notifier l'admin
    admin = db.query(UserModel).filter(UserModel.role == RoleEnum.ADMIN).first()
    if admin:
        db.add(NotificationModel(
            user_id=admin.id,
            titre="Production acceptée",
            message=f"L'agriculteur a accepté de produire {demande.nom_produit} pour le client."
        ))

    # 3. Notifier le client avec les coordonnées de l'agriculteur
    agr_user = relance.agriculteur.user
    client_user = demande.client.user
    db.add(NotificationModel(
        user_id=client_user.id,
        titre="Production en cours !",
        message=f"Votre demande pour {demande.nom_produit} a été acceptée par {agr_user.prenom} {agr_user.nom}. Contact: {agr_user.telephone} / {agr_user.email}. Prévu pour le {demande.date_limite}."
    ))

    db.commit()
    return {"message": "Vous avez accepté la production. Le client et l'admin ont été notifiés."}

@router.get("/demandes", response_model=List[DemandeProductionRead])
def lister_demandes(db: Session = Depends(get_db)):
    return db.query(DemandeProductionModel).all()
