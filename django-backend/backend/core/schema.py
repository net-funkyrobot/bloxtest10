from datetime import datetime

from ninja import Schema
from pydantic import EmailStr


class FirestoreUserProfile(Schema):
    email: EmailStr
    created: datetime
