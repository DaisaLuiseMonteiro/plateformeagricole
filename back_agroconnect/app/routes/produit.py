from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.models.produit_model import ProduitModel, StatutPublicationEnum
from app.models.user_model import UserModel, RoleEnum, AgriculteurModel
from app.models.notification_model import NotificationModel
from app.schemas.produit_schema import ProduitCreate, ProduitRead, ProduitUpdate
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/produits",
    tags=["Produits"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def ajouter_produit(produit_data: ProduitCreate, db: Session = Depends(get_db)):
    try:
        agriculteur = db.query(AgriculteurModel).filter(AgriculteurModel.id == produit_data.agriculteur_id).first()
        if not agriculteur or not agriculteur.is_actif:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agriculteur introuvable ou inactif"
            )

        # 1. Création du produit
        nouveau_produit = ProduitModel(
            prix_unitaire=produit_data.prix_unitaire,
            description=produit_data.description,
            quantite_stock=produit_data.quantite_stock,
            photo=produit_data.photo,
            categorie=produit_data.categorie,
            agriculteur_id=produit_data.agriculteur_id,
            statut_publication=StatutPublicationEnum.EN_ATTENTE
        )
        
        db.add(nouveau_produit)
        db.commit()
        db.refresh(nouveau_produit)
        
        # 2. Création de la notification pour l'administrateur
        admin = db.query(UserModel).filter(UserModel.role == RoleEnum.ADMIN).first()
        if admin:
            import json
            nouvelle_notif = NotificationModel(
                user_id=admin.id,
                titre="Nouveau produit à valider",
                message=f"L'agriculteur a ajouté {nouveau_produit.categorie}: {nouveau_produit.description or 'Produit'}",
                type="action_required",
                data=json.dumps({"produit_id": nouveau_produit.id, "type": "product_validation"})
            )
            db.add(nouvelle_notif)
            db.commit()
        
        return {
            "message": "Le produit est bien enregistré.",
            "details": "Jusqu'à maximum 2h de temps, vous serez informé si l'administrateur a autorisé la publication du produit sur la plateforme ou non.",
            "produit": nouveau_produit 
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"CRASH BACKEND: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur : {str(e)}"
        )

    return produits


@router.get("/agriculteur/{agriculteur_id}", response_model=list[ProduitRead])
def lister_produits_agriculteur(agriculteur_id: str, db: Session = Depends(get_db)):
    produits = db.query(ProduitModel).filter(
        ProduitModel.agriculteur_id == agriculteur_id
    ).all()
    return produits


@router.put("/{produit_id}", response_model=ProduitRead)
def modifier_produit(
    produit_id: str,
    produit_data: ProduitUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.AGRICULTEUR or not current_user.agriculteur:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul un agriculteur peut modifier un produit."
        )

    produit = db.query(ProduitModel).filter(ProduitModel.id == produit_id).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé."
        )

    if produit.agriculteur_id != current_user.agriculteur.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez modifier que vos propres produits."
        )

    update_data = produit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(produit, field, value)

    db.commit()
    db.refresh(produit)

    return produit


@router.delete("/{produit_id}", status_code=status.HTTP_200_OK)
def supprimer_produit(
    produit_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.AGRICULTEUR or not current_user.agriculteur:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul un agriculteur peut supprimer un produit."
        )

    produit = db.query(ProduitModel).filter(ProduitModel.id == produit_id).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé."
        )

    if produit.agriculteur_id != current_user.agriculteur.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez supprimer que vos propres produits."
        )

    db.delete(produit)
    db.commit()

    return {"message": "Produit supprimé avec succès."}


@router.patch("/{produit_id}/publier")
def valider_publication(
    produit_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul un administrateur peut valider une publication."
        )

    produit = db.query(ProduitModel).filter(ProduitModel.id == produit_id).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé."
        )

    produit.statut_publication = StatutPublicationEnum.PUBLIE
    
    # Notifier l'agriculteur
    agriculteur_user = db.query(UserModel).filter(UserModel.id == produit.agriculteur.user_id).first()
    if agriculteur_user:
        nouvelle_notif = NotificationModel(
            user_id=agriculteur_user.id,
            titre="Produit validé",
            message=f"Votre produit '{produit.description or 'Produit'}' a été validé et est maintenant en ligne !",
            type="info"
        )
        db.add(nouvelle_notif)

    db.commit()
    return {"message": "Produit validé et publié avec succès."}


@router.patch("/{produit_id}/rejeter")
def rejeter_publication(
    produit_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul un administrateur peut rejeter une publication."
        )

    produit = db.query(ProduitModel).filter(ProduitModel.id == produit_id).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit non trouvé."
        )

    produit.statut_publication = StatutPublicationEnum.REJETE
    
    # Notifier l'agriculteur
    agriculteur_user = db.query(UserModel).filter(UserModel.id == produit.agriculteur.user_id).first()
    if agriculteur_user:
        nouvelle_notif = NotificationModel(
            user_id=agriculteur_user.id,
            titre="Produit rejeté",
            message=f"Votre produit '{produit.description or 'Produit'}' a été rejeté par l'administration.",
            type="info"
        )
        db.add(nouvelle_notif)

    db.commit()
    return {"message": "Produit rejeté avec succès."}
