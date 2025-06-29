from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Request
from limits.strategies import RateLimiter
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
        request: Request,
        body: ContactCreate,
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    return await repository_contacts.create_contact(body, current_user, db)


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
        name: str | None = None,
        surname: str | None = None,
        email: str | None = None,
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.search_contacts(name, surname, email, current_user, db)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse])
async def upcoming_birthdays(
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.get_upcoming_birthdays(current_user, db)
    return contacts


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
        contact_id: int,
        body: ContactUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact