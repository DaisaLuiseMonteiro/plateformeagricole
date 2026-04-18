from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Importations relatives selon votre structure
from database import get_db
from app.models.user_model import UserModel, RoleEnum, AgriculteurModel, ClientModel
from app.models.RefreshToken import RefreshToken
from app.schemas.user_schema import UserCreate, UserRead, AgriculteurRead, ClientRead, ChangePasswordRequest, LogoutRequest, ResetPasswordRequest

from utils.security import hash_password, verify_password, create_access_token, create_refresh_token
from utils.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Vérifier si l'utilisateur existe déjà
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà enregistré."
        )

    # 2. Créer l'entité de base utilisateur
    new_user = UserModel(
        nom=user_data.nom,
        prenom=user_data.prenom,
        email=user_data.email,
        mot_de_pass=hash_password(user_data.mot_de_pass),  
        telephone=user_data.telephone,
        role=user_data.role,
        photo=user_data.photo
    )
    
    db.add(new_user)
    db.flush()

    # 3. Créer le profil spécifique selon le rôle
    if user_data.role == RoleEnum.AGRICULTEUR:
        profil = AgriculteurModel(user_id=new_user.id)
    elif user_data.role == RoleEnum.CLIENT:
        profil = ClientModel(user_id=new_user.id)

    db.add(profil)
    db.commit()       
    db.refresh(new_user)

    return new_user

# Schema pour le Login
class UserLogin(BaseModel):
    email: str
    mot_de_pass: str

@router.post("/login")
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.mot_de_pass, user.mot_de_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect."
        )
        
    # 3. Créer les tokens
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token_str = create_refresh_token(data={"sub": user.id})

    # 4. Enregistrer le refresh token en DB
    expire_date = datetime.utcnow() + timedelta(days=7)
    new_refresh_token = RefreshToken(token=refresh_token_str, user_id=user.id, expires_at=expire_date)
    db.add(new_refresh_token)
    db.commit()

    # 5. Préparer la réponse
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token_str,
        "message": f"vous vous etes connecte en tant k {user.role.value}",
        "user_id": user.id,
        "role": user.role.value,
        "photo": user.photo
    }

    if user.role == RoleEnum.AGRICULTEUR and user.agriculteur:
        response_data["agriculteur_id"] = user.agriculteur.id
    elif user.role == RoleEnum.CLIENT and user.client:
        response_data["client_id"] = user.client.id
        
    return response_data

class TokenRefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    token_record = db.query(RefreshToken).filter(RefreshToken.token == request.refresh_token).first()
    
    if not token_record:
        raise HTTPException(status_code=401, detail="Refresh token invalide")
        
    if token_record.expires_at and token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expiré")
        
    user = token_record.user
    new_access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout_user(request: LogoutRequest, db: Session = Depends(get_db)):
    token_record = db.query(RefreshToken).filter(RefreshToken.token == request.refresh_token).first()
    if not token_record:
        raise HTTPException(status_code=400, detail="Token invalide ou déjà déconnecté")
    
    db.delete(token_record)
    db.commit()
    
    return {"message": "Déconnexion réussie"}

@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not verify_password(request.old_password, current_user.mot_de_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ancien mot de passe incorrect."
        )
    
    current_user.mot_de_pass = hash_password(request.new_password)
    db.commit()
    
    return {"message": "Mot de passe modifié avec succès"}

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest, 
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cet email est inexistant."
        )
    
    user.mot_de_pass = hash_password(request.nouveau_mot_de_pass)
    db.commit()
    
    return {"message": "Mot de passe réinitialisé avec succès."}

@router.put("/agriculteurs/{id}/desactiver")
def desactiver_agriculteur(
    id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé. Seul un administrateur peut désactiver un agriculteur."
        )
    agriculteur = db.query(AgriculteurModel).filter(AgriculteurModel.id == id).first()
    if not agriculteur:
        raise HTTPException(status_code=404, detail="Agriculteur non trouvé")
    
    agriculteur.is_actif = False
    db.commit()
    
    return {"message": "Agriculteur désactivé avec succès"}

@router.put("/agriculteurs/{id}/activer")
def activer_agriculteur(
    id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé. Seul un administrateur peut activer un agriculteur."
        )
    agriculteur = db.query(AgriculteurModel).filter(AgriculteurModel.id == id).first()
    if not agriculteur:
        raise HTTPException(status_code=404, detail="Agriculteur non trouvé")
    
    agriculteur.is_actif = True
    db.commit()
    
    return {"message": "Agriculteur activé avec succès"}

@router.get("/agriculteurs", response_model=list[AgriculteurRead])
def lister_agriculteurs(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé. Seul un administrateur peut voir cette liste."
        )
    
    return db.query(AgriculteurModel).all()

@router.get("/clients", response_model=list[ClientRead])
def lister_clients(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé. Seul un administrateur peut voir cette liste."
        )
    
    return db.query(ClientModel).all()

