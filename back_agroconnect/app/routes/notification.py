from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.models.notification_model import NotificationModel
from app.schemas.notification_schema import NotificationRead

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/user/{user_id}", response_model=List[NotificationRead])
def get_user_notifications(user_id: str, db: Session = Depends(get_db)):
    return db.query(NotificationModel).filter(
        NotificationModel.user_id == user_id
    ).order_by(NotificationModel.date_creation.desc()).all()

@router.patch("/{notif_id}/lire")
def mark_as_read(notif_id: str, db: Session = Depends(get_db)):
    notif = db.query(NotificationModel).filter(NotificationModel.id == notif_id).first()
    if notif:
        notif.est_lue = True
        db.commit()
        return {"message": "Notification marquée comme lue"}
    return {"message": "Notification introuvable"}

@router.patch("/user/{user_id}/lire-tout")
def mark_all_as_read(user_id: str, db: Session = Depends(get_db)):
    db.query(NotificationModel).filter(
        NotificationModel.user_id == user_id,
        NotificationModel.est_lue == False
    ).update({"est_lue": True}, synchronize_session=False)
    db.commit()
    return {"message": "Toutes les notifications ont été marquées comme lues"}