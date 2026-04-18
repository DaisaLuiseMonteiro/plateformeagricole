import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship
from database import Base


class RoleEnum(str, Enum):
    ADMIN       = "admin"
    CLIENT      = "client"
    AGRICULTEUR = "agriculteur"


class UserModel(Base):
    __tablename__ = "users"

    id          = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nom         = Column(String, nullable=False)
    prenom      = Column(String, nullable=False)
    mot_de_pass = Column(String, nullable=False)
    telephone   = Column(String, nullable=True)
    role        = Column(SAEnum(RoleEnum), nullable=False)
    email       = Column(String, unique=True, nullable=False)
    photo       = Column(String, nullable=True)

    # Relations
    agriculteur = relationship("AgriculteurModel", back_populates="user", uselist=False)
    client      = relationship("ClientModel",      back_populates="user", uselist=False)
    admin       = relationship("AdministrateurModel", back_populates="user", uselist=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class AgriculteurModel(Base):
    __tablename__ = "agriculteurs"

    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    localisation = Column(String, nullable=True)
    is_actif     = Column(Boolean, default=True)

    # Clé étrangère → User
    user_id      = Column(String, ForeignKey("users.id"), nullable=False, unique=True)

    # Relations
    user         = relationship("UserModel",    back_populates="agriculteur")
    produits     = relationship("ProduitModel", back_populates="agriculteur")


class ClientModel(Base):
    __tablename__ = "clients"

    id      = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    adresse = Column(String, nullable=True)

    # Clé étrangère → User
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)

    # Relations
    user      = relationship("UserModel",     back_populates="client")
    commandes = relationship("CommandeModel", back_populates="client")


class AdministrateurModel(Base):
    __tablename__ = "administrateurs"

    id      = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Clé étrangère → User
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)

    # Relations
    user = relationship("UserModel", back_populates="admin")