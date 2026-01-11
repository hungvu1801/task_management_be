from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import Any


router = APIRouter(prefix="/project", tags=["project"])
