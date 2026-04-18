import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NotificationModel(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    titre = Column(String, nullable=True)
    message = Column(String, nullable=False)
    type = Column(String, default="info") # info, action_required
    data = Column(String, nullable=True) # Stockage JSON (ex: {"produit_id": "...", "type": "production_request"})
    est_lu = Column(Boolean, default=False)
    date_creation = Column(DateTime, default=datetime.utcnow)