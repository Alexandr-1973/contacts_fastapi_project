from sqlalchemy import Column, Integer, String, Date, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    """
    SQLAlchemy model for a contact entry.

    Attributes:
        id (int): Primary key.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Unique email of the contact.
        phone_number (str): Unique phone number.
        birthday (date): Date of birth.
        created_at (datetime): Timestamp of creation.
        add_info (str): Additional information about the contact.
        user_id (int): Foreign key referencing the associated user.
        user (User): Relationship to the User model.
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(30), unique=True)
    birthday = Column(Date)
    created_at = Column('created_at', DateTime, default=func.now())
    add_info = Column(String)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")

class User(Base):
    """
    SQLAlchemy model for a user account.

    Attributes:
        id (int): Primary key.
        username (str): Username.
        email (str): Unique email address.
        password (str): Hashed password.
        created_at (datetime): Timestamp of creation.
        avatar (str): URL to avatar image.
        refresh_token (str): Refresh token for JWT authentication.
        confirmed (bool): Email confirmation status.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed= Column(Boolean(), default=False, nullable=True)
