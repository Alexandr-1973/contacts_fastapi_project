from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from fastapi_project.src.database.models import Contact, User
from fastapi_project.src.schemas import ContactSchema

async def get_contacts(limit: int, offset: int, use_get_filters: dict, db: AsyncSession, user: User):
    filters_list=[getattr(Contact,k)==v for k,v in use_get_filters.items()]
    stmt = select(Contact).filter(and_(*filters_list, Contact.user_id == user.id )).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_birthdays_contacts(limit: int, offset: int, days: int, db: AsyncSession, user: User):
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
    stmt = select(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id))
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)  # (title=body.title, description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
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
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact