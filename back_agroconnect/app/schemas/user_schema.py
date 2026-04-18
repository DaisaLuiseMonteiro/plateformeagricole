from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user_model import RoleEnum


# ============================================================
# USER SCHEMAS
# ============================================================

class UserCreate(BaseModel):
    nom         : str
    prenom      : str
    email       : str
    mot_de_pass : str
    telephone   : Optional[str] = None
    role        : RoleEnum
    photo       : Optional[str] = None


class UserUpdate(BaseModel):
    nom       : Optional[str] = None
    prenom    : Optional[str] = None
    telephone : Optional[str] = None
    email     : Optional[str] = None
    photo     : Optional[str] = None


class UserRead(BaseModel):
    id     : str
    nom    : str
    prenom : str
    email  : str
    role   : RoleEnum
    photo  : Optional[str] = None

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    old_password : str
    new_password : str


class LogoutRequest(BaseModel):
    refresh_token : str


class ResetPasswordRequest(BaseModel):
    email : str
    nouveau_mot_de_pass : str


# ============================================================
# AGRICULTEUR SCHEMAS
# ============================================================

class AgriculteurCreate(BaseModel):
    localisation : Optional[str] = None
    user_id      : str


class AgriculteurUpdate(BaseModel):
    localisation : Optional[str] = None


class AgriculteurRead(BaseModel):
    id           : str
    localisation : Optional[str]
    is_actif     : Optional[bool] = True
    user_id      : str
    user         : Optional[UserRead] = None

    class Config:
        from_attributes = True


# ============================================================
# CLIENT SCHEMAS
# ============================================================

class ClientCreate(BaseModel):
    adresse : Optional[str] = None
    user_id : str


class ClientUpdate(BaseModel):
    adresse : Optional[str] = None


class ClientRead(BaseModel):
    id      : str
    adresse : Optional[str]
    user_id : str
    user    : Optional[UserRead] = None

    class Config:
        from_attributes = True


# ============================================================
# ADMINISTRATEUR SCHEMAS
# ============================================================

class AdministrateurCreate(BaseModel):
    user_id : str


class AdministrateurUpdate(BaseModel):
    user_id : Optional[str] = None


class AdministrateurRead(BaseModel):
    id      : str
    user_id : str
    user    : Optional[UserRead] = None

    class Config:
        from_attributes = True