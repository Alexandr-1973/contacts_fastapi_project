from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    """
     Schema for creating and validating contact information.

     :param first_name: First name of the contact.
     :type first_name: str
     :param last_name: Last name of the contact.
     :type last_name: str
     :param email: Email address of the contact.
     :type email: EmailStr
     :param phone_number: Contact's phone number.
     :type phone_number: str
     :param birthday: Birthday date of the contact.
     :type birthday: date
     :param add_info: Optional additional information about the contact.
     :type add_info: Optional[str]
     """
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    email: EmailStr
    phone_number: str = Field(max_length=30)
    birthday : date
    add_info: Optional[str]=''


class ContactResponseSchema(ContactSchema):
    """
    Schema for returning contact information with ID and timestamp.

    Inherits all fields from :class:`ContactSchema`.

    :param id: Unique identifier of the contact.
    :type id: int
    :param created_at: Timestamp when the contact was created.
    :type created_at: datetime
    """
    id: int = 1
    created_at: datetime

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    """
    Schema for user registration input.

    :param username: Desired username of the user.
    :type username: str
    :param email: User's email address.
    :type email: EmailStr
    :param password: User's password.
    :type password: str
    """
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    """
    Schema for returning user information.

    :param id: Unique user ID.
    :type id: int
    :param username: User's display name.
    :type username: str
    :param email: Email address of the user.
    :type email: EmailStr
    :param avatar: URL to the user's avatar image.
    :type avatar: str
    """
    id: int = 1
    username: str
    email: EmailStr
    avatar: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    """
    Schema for access and refresh tokens returned on authentication.

    :param access_token: The access token for authentication.
    :type access_token: str
    :param refresh_token: The refresh token to obtain a new access token.
    :type refresh_token: str
    :param token_type: Type of the token, default is "bearer".
    :type token_type: str
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    """
    Schema for requesting operations based on email.

    :param email: Email address to perform the request on.
    :type email: EmailStr
    """
    email: EmailStr