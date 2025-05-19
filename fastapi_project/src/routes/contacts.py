from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi_project.src.database.db import get_db
from fastapi_project.src.repository import contacts as repositories_contacts
from fastapi_project.src.schemas import ContactSchema, ContactResponseSchema
from fastapi_project.src.database.models import User
from fastapi_project.src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get("/", response_model=list[ContactResponseSchema], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60, identifier=auth_service.get_email_from_request))])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
        first_name: Optional[str] = Query(None),
        last_name: Optional[str] = Query(None),
        email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)
):
    """
    Retrieve a list of contacts with optional filters.

    :param limit: Maximum number of contacts to return. Must be between 10 and 500.
    :type limit: int
    :param offset: Number of records to skip.
    :type offset: int
    :param first_name: Filter contacts by first name.
    :type first_name: Optional[str]
    :param last_name: Filter contacts by last name.
    :type last_name: Optional[str]
    :param email: Filter contacts by email.
    :type email: Optional[str]
    :param db: Database session.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: List of contacts.
    :rtype: list[ContactResponseSchema]
    """
    get_filters = {"first_name": first_name, "last_name": last_name, "email": email}
    use_get_filters={k:v for k,v in get_filters.items() if v}
    contacts = await repositories_contacts.get_contacts(limit, offset, use_get_filters, db, current_user)
    return contacts

@router.get("/birthday", response_model=list[ContactResponseSchema])
async def get_contacts_by_birthday(limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0), days: int = Query(7, ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve contacts with birthdays within a number of upcoming days.

    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param offset: Number of records to skip.
    :type offset: int
    :param days: Number of upcoming days to check for birthdays.
    :type days: int
    :param db: Database session.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: List of contacts with upcoming birthdays.
    :rtype: list[ContactResponseSchema]
    """
    contacts = await repositories_contacts.get_birthdays_contacts(limit, offset, days, db, current_user)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponseSchema)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a specific contact by ID.

    :param contact_id: ID of the contact.
    :type contact_id: int
    :param db: Database session.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :raises HTTPException: If contact not found.
    :return: Contact details.
    :rtype: ContactResponseSchema
    """
    contact = await repositories_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponseSchema, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60, identifier=auth_service.get_email_from_request))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Create a new contact.

    :param body: Contact data to create.
    :type body: ContactSchema
    :param db: Database session.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: Created contact.
    :rtype: ContactResponseSchema
    """
    contact = await repositories_contacts.create_contact(body, db, current_user)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Update a contact by ID.

    :param body: Updated contact data.
    :type body: ContactSchema
    :param contact_id: ID of the contact to update.
    :type contact_id: int
    :param db: Database session.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :raises HTTPException: If contact not found.
    :return: Updated contact.
    """
    contact = await repositories_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete a contact by ID.

    :param contact_id: ID of the contact to delete.
    :type contact_id: int
    :param db: Database session.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: None
    """
    contact = await repositories_contacts.delete_contact(contact_id, db, current_user)
    return contact

