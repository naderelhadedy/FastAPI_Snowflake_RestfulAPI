"""
Models module
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    """
    ClientBase
    """
    name: str
    email: str


class ClientUpdate(BaseModel):
    """
    ClientUpdate
    """
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        extra = "forbid"  # Forbid unknown fields


class ClientResponse(ClientBase):
    """
    ClientResponse
    """
    id: int
    created_at: datetime
