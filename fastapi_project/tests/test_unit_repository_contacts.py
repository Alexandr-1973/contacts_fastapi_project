import unittest
from unittest.mock import MagicMock, AsyncMock, Mock
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.src.database.models import Contact, User
from fastapi_project.src.schemas import ContactSchema
from fastapi_project.src.repository.contacts import (
    create_contact,
    get_contact,
    update_contact,
    delete_contact,
    get_contacts,
    get_birthdays_contacts,
)


class TestAsyncTodo(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username="test_user", password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)
        self.test_contacts = [
            Contact(
                id=1,
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone_number="1234567890",
                birthday=date.today() + timedelta(days=3),
                user=self.user,
            ),
            Contact(
                id=2,
                first_name="Vasya",
                last_name="Doej",
                email="vasya.doej@example.com",
                phone_number="1234567888",
                birthday=date.today() - timedelta(days=3),
                user=self.user,
            ),
        ]
        self.test_body = ContactSchema(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            birthday="1990-01-01",
        )

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = self.test_contacts
        mocked_contacts = Mock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        filters = {"first_name": None, "last_name": None, "email": None}
        result = await get_contacts(limit, offset, filters, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_birthdays_contacts(self):
        mocked_result = MagicMock()
        mocked_result.scalars.return_value.all.return_value = self.test_contacts
        self.session.execute.return_value = mocked_result
        result = await get_birthdays_contacts(
            limit=10, offset=0, days=7, db=self.session, user=self.user
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, "John")

    async def test_get_contact_found(self):
        mocked_result = MagicMock()
        mocked_result.scalar_one_or_none.return_value = self.test_contacts[0]
        self.session.execute.return_value = mocked_result
        result = await get_contact(1, self.session, self.user)
        self.session.execute.assert_awaited_once()
        self.assertEqual(result, self.test_contacts[0])

    async def test_get_contact_not_found(self):
        mocked_result = MagicMock()
        mocked_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_result
        result = await get_contact(3, self.session, self.user)
        self.session.execute.assert_awaited_once()
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = self.test_body
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)

    async def test_update_contact_found(self):
        mocked_result = MagicMock()
        mocked_result.scalar_one_or_none.return_value = self.test_contacts[0]
        self.session.execute.return_value = mocked_result
        result = await update_contact(
            self.test_contacts[0].id, self.test_body, self.session, self.user
        )
        self.session.execute.assert_awaited_once()
        self.session.commit.assert_awaited_once()
        self.session.refresh.assert_awaited_once_with(self.test_contacts[0])
        self.assertEqual(result.first_name, self.test_body.first_name)
        self.assertEqual(result.last_name, self.test_body.last_name)
        self.assertEqual(result.email, self.test_body.email)
        self.assertEqual(result.phone_number, self.test_body.phone_number)
        self.assertEqual(result.birthday, self.test_body.birthday)

    async def test_update_contact_not_found(self):
        mocked_result = MagicMock()
        mocked_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_result
        result = await update_contact(
            self.test_contacts[0].id, self.test_body, self.session, self.user
        )
        self.session.execute.assert_awaited_once()
        self.session.commit.assert_not_awaited()
        self.session.refresh.assert_not_awaited()
        self.assertIsNone(result)

    async def test_delete_contact_found(self):
        mocked_result = MagicMock()
        mocked_result.scalar_one_or_none.return_value = self.test_contacts[0]
        self.session.execute.return_value = mocked_result
        result = await delete_contact(self.test_contacts[0].id, self.session, self.user)
        self.session.delete.assert_awaited_once_with(self.test_contacts[0])
        self.session.commit.assert_awaited_once()
        self.assertEqual(result, self.test_contacts[0])

    async def test_delete_contact_not_found(self):
        mocked_result = MagicMock()
        mocked_result.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_result
        result = await delete_contact(self.test_contacts[0].id, self.session, self.user)
        self.session.delete.assert_not_awaited()
        self.session.commit.assert_not_awaited()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
