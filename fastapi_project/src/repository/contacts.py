from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from fastapi_project.src.database.models import Contact, User
from fastapi_project.src.schemas import ContactSchema

async def get_contacts(limit: int, offset: int, use_get_filters: dict, db: AsyncSession, user: User):
    """
    Retrieve a list of contacts filtered by parameters and scoped to the given user.

    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param offset: Number of contacts to skip (for pagination).
    :type offset: int
    :param use_get_filters: Dictionary of filters where keys are Contact model field names and values are expected values.
    :type use_get_filters: dict
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :param user: The user whose contacts should be retrieved.
    :type user: User
    :return: List of Contact objects matching the filters.
    :rtype: list[Contact]
    """
    filters_list=[getattr(Contact,k)==v for k,v in use_get_filters.items()]
    stmt = select(Contact).filter(and_(*filters_list, Contact.user_id == user.id )).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_birthdays_contacts(limit: int, offset: int, days: int, db: AsyncSession, user: User):
    """
    Retrieve contacts whose birthdays fall within the given number of days from today.

    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param offset: Number of contacts to skip (for pagination).
    :type offset: int
    :param days: Range in days to look ahead for upcoming birthdays.
    :type days: int
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :param user: The user whose contacts should be checked.
    :type user: User
    :return: List of Contact objects with upcoming birthdays.
    :rtype: list[Contact]
    """
    stmt=select(Contact).filter(Contact.user_id == user.id)
    contacts = await db.execute(stmt)
    today = date.today()
    upcoming_birthdays_list = []
    for contact in contacts.scalars().all():
        if contact.birthday:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            if 0 <= (birthday_this_year - today).days <= days:
                upcoming_birthdays_list.append(contact)
    return upcoming_birthdays_list[offset:offset+limit]


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    Retrieve a single contact by ID, ensuring it belongs to the given user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :param user: The user who owns the contact.
    :type user: User
    :return: The Contact object if found, otherwise None.
    :rtype: Contact or None
    """
    stmt = select(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id))
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    Create a new contact associated with the given user.

    :param body: Schema with contact data.
    :type body: ContactSchema
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :param user: The user who owns the new contact.
    :type user: User
    :return: The created Contact object.
    :rtype: Contact
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)  # (title=body.title, description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    """
    Update an existing contact owned by the user.

    :param contact_id: ID of the contact to update.
    :type contact_id: int
    :param body: Schema with updated contact data.
    :type body: ContactSchema
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :param user: The user who owns the contact.
    :type user: User
    :return: The updated Contact object or None if not found.
    :rtype: Contact or None
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        for key, value in body.model_dump().items():
            setattr(contact, key, value)
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    Delete a contact by ID if it belongs to the user.

    :param contact_id: ID of the contact to delete.
    :type contact_id: int
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :param user: The user who owns the contact.
    :type user: User
    :return: The deleted Contact object or None if not found.
    :rtype: Contact or None
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


