from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.models.commande_model import CommandeModel, DetailsModel, StatutEnum
from app.models.user_model import UserModel, RoleEnum
from app.models.produit_model import ProduitModel
from app.schemas.commande_schema import CommandeCreate, CommandeRead, CommandeUpdate
from app.models.notification_model import NotificationModel
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/commandes",
    tags=["Commandes"]
)

@router.post("/", response_model=CommandeRead, status_code=status.HTTP_201_CREATED)
def creer_commande(commande_data: CommandeCreate, db: Session = Depends(get_db)):
    # 1. Création de la commande de base
    nouvelle_commande = CommandeModel(
        client_id=commande_data.client_id,
        montant_commande=commande_data.montant_total,
        statut=StatutEnum.EN_ATTENTE
    )
    db.add(nouvelle_commande)
    db.flush()

    # 2. Création des détails
    for item in commande_data.items:
        detail = DetailsModel(
            commande_id=nouvelle_commande.id,
            produit_id=item.produit_id,
            quantite=item.quantite,
            montant=item.montant
        )
        db.add(detail)
    
    db.commit()
    db.refresh(nouvelle_commande)

    # 3. Notification pour l'administrateur
    admin = db.query(UserModel).filter(UserModel.role == RoleEnum.ADMIN).first()
    if admin:
        import json
        nouvelle_notif = NotificationModel(
            user_id=admin.id,
            titre="Nouvelle commande reçue",
            message=f"Une nouvelle commande de {nouvelle_commande.montant_commande} CFA a été passée.",
            type="action_required",
            data=json.dumps({"commande_id": nouvelle_commande.id, "type": "order_validation"})
        )
        db.add(nouvelle_notif)
        db.commit()

    return nouvelle_commande

@router.get("/client/{client_id}", response_model=List[CommandeRead])
def lister_commandes_client(client_id: str, db: Session = Depends(get_db)):
    return db.query(CommandeModel).filter(CommandeModel.client_id == client_id).all()

@router.get("/agriculteur/{agriculteur_id}", response_model=List[CommandeRead])
def lister_commandes_agriculteur(agriculteur_id: str, db: Session = Depends(get_db)):
    # On récupère les commandes qui contiennent au moins un produit de cet agriculteur
    return db.query(CommandeModel).join(DetailsModel).join(ProduitModel).filter(
        ProduitModel.agriculteur_id == agriculteur_id
    ).all()

@router.get("/admin", response_model=List[CommandeRead])
def lister_toutes_commandes(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administrateur")
    return db.query(CommandeModel).all()

@router.patch("/{commande_id}/confirmer", response_model=CommandeRead)
def confirmer_commande(commande_id: str, db: Session = Depends(get_db)):
    commande = db.query(CommandeModel).filter(CommandeModel.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    # 1. Mise à jour du statut
    commande.statut = StatutEnum.CONFIRMEE
    
    # 2. Mise à jour du stock (Diminution)
    try:
        for detail in commande.details:
            produit = detail.produit
            if produit.quantite_stock < detail.quantite:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuffisant pour le produit {produit.description or produit.id}"
                )
            produit.quantite_stock -= detail.quantite
        
        # 3. Notification au client
        client_user = db.query(UserModel).filter(UserModel.id == commande.client.user_id).first()
        if client_user:
            nouvelle_notif = NotificationModel(
                user_id=client_user.id,
                titre="Commande confirmée",
                message=f"Votre commande #{commande.id[:8]} a été confirmée par l'administration.",
                type="info"
            )
            db.add(nouvelle_notif)

        db.commit()
        db.refresh(commande)
        return commande
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{commande_id}/rejeter", response_model=CommandeRead)
def rejeter_commande(commande_id: str, db: Session = Depends(get_db)):
    commande = db.query(CommandeModel).filter(CommandeModel.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    ancien_statut = commande.statut
    commande.statut = StatutEnum.ANNULEE
    
    # Si la commande était déjà confirmée, on rend le stock
    if ancien_statut == StatutEnum.CONFIRMEE or ancien_statut == StatutEnum.VALIDEE:
        for detail in commande.details:
            produit = detail.produit
            produit.quantite_stock += detail.quantite

    # Notification au client
    client_user = db.query(UserModel).filter(UserModel.id == commande.client.user_id).first()
    if client_user:
        nouvelle_notif = NotificationModel(
            user_id=client_user.id,
            titre="Commande rejetée/annulée",
            message=f"Désolé, votre commande #{commande.id[:8]} a été rejetée ou annulée.",
            type="info"
        )
        db.add(nouvelle_notif)

    db.commit()
    db.refresh(commande)
    return commande

@router.patch("/{commande_id}/valider", response_model=CommandeRead)
def valider_reception_commande(commande_id: str, db: Session = Depends(get_db)):
    commande = db.query(CommandeModel).filter(CommandeModel.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    commande.statut = StatutEnum.VALIDEE
    db.commit()
    db.refresh(commande)
    return commande
