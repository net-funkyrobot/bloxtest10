from datetime import datetime
from typing import Generic, Optional, TypeVar

from ninja import Schema
from pydantic import EmailStr

ReturnType = TypeVar('ReturnType')


class ServiceResult(Schema, Generic[ReturnType]):
    success: bool
    return_value: Optional[ReturnType]
    errors: Optional[list[Exception]]

    class Config:
        arbitrary_types_allowed = True


class FirestoreUserProfile(Schema):
    email: EmailStr
    created: datetime
