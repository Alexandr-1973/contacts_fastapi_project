from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar
from fastapi_project.src.database.db import get_db
from fastapi_project.src.database.models import User
from fastapi_project.src.schemas import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user from the database by email.

    :param email: Email address of the user.
    :type email: str
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :return: User object if found, else None.
    :rtype: User or None
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new user with optional Gravatar avatar.

    :param body: Schema with user registration data.
    :type body: UserSchema
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :return: The newly created User object.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print("avatar = None")
        # avatar = None

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update a user's refresh token.

    :param user: User object to update.
    :type user: User
    :param token: New refresh token or None.
    :type token: str or None
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    """
    user.refresh_token = token
    await db.commit()

async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Set a user's confirmed email flag to True.

    :param email: Email address of the user.
    :type email: str
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Update the avatar URL of a user.

    :param email: Email address of the user.
    :type email: str
    :param url: New avatar URL or None.
    :type url: str or None
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    :return: Updated User object.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_password(user: User, hash_password, db: AsyncSession):
    """
    Update a user's password (already hashed).

    :param user: User object to update.
    :type user: User
    :param hash_password: Hashed password string.
    :type hash_password: str
    :param db: Async SQLAlchemy session.
    :type db: AsyncSession
    """
    user.password = hash_password
    await db.commit()

