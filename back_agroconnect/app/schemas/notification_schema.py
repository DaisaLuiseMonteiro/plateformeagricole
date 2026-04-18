from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str
    message: str

class NotificationRead(BaseModel):
    id: str
    user_id: str
    message: str
    est_lu: bool
    date_creation: datetime

    class Config:
        from_attributes = True
