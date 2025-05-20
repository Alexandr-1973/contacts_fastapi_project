import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi_project.src.database.models import User
from fastapi_project.src.schemas import UserSchema
from fastapi_project.src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar_url,
    update_user_password
)

class TestUserRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_db = AsyncMock()
        self.test_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashedpassword",
            avatar=None,
            refresh_token=None,
            confirmed=False
        )
        self.user_schema = UserSchema(
            username="testuser",
            email="test@example.com",
            password="hashedpw"
        )

    async def test_get_user_by_email_found(self):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.test_user
        self.mock_db.execute.return_value = mock_result
        user = await get_user_by_email("test@example.com", self.mock_db)
        self.mock_db.execute.assert_awaited_once()
        self.assertEqual(user, self.test_user)
        mock_result.scalar_one_or_none.assert_called_once()

    async def test_get_user_by_email_not_found(self):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result
        user = await get_user_by_email("not_found@example.com", self.mock_db)
        self.mock_db.execute.assert_awaited_once()
        self.assertIsNone(user)
        mock_result.scalar_one_or_none.assert_called_once()


    @patch("fastapi_project.src.repository.users.Gravatar")
    async def test_create_user_success(self, mock_gravatar):
        gravatar_instance = mock_gravatar.return_value
        gravatar_instance.get_image.return_value = "avatar_url"
        self.mock_db.add = MagicMock()
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        user = await create_user(self.user_schema, self.mock_db)
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_awaited_once()
        self.mock_db.refresh.assert_awaited_once()
        self.assertIsInstance(user, User)
        self.assertEqual(user.avatar, "avatar_url")

    @patch("fastapi_project.src.repository.users.Gravatar")
    async def test_create_user_gravatar_exception(self, mock_gravatar):
        gravatar_instance = mock_gravatar.return_value
        gravatar_instance.get_image.side_effect = Exception("error")
        self.mock_db.add = MagicMock()
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        user = await create_user(self.user_schema, self.mock_db)
        self.assertIsInstance(user, User)
        self.assertIsNone(user.avatar)

    async def test_update_token(self):
        self.mock_db.commit = AsyncMock()
        await update_token(self.test_user, "new_token", self.mock_db)
        self.assertEqual(self.test_user.refresh_token, "new_token")
        self.mock_db.commit.assert_awaited_once()

    async def test_confirmed_email(self):
        self.mock_db.commit = AsyncMock()
        with patch(
            "fastapi_project.src.repository.users.get_user_by_email",
            new=AsyncMock(return_value=self.test_user)
        ):
            await confirmed_email("test@example.com", self.mock_db)

        self.assertTrue(self.test_user.confirmed)
        self.mock_db.commit.assert_awaited_once()

    async def test_update_avatar_url(self):
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        with patch(
            "fastapi_project.src.repository.users.get_user_by_email",
            new=AsyncMock(return_value=self.test_user)
        ):
            updated_user = await update_avatar_url("test@example.com", "new_avatar_url", self.mock_db)

        self.assertEqual(updated_user.avatar, "new_avatar_url")
        self.mock_db.commit.assert_awaited_once()
        self.mock_db.refresh.assert_awaited_once()

    async def test_update_user_password(self):
        self.mock_db.commit = AsyncMock()
        await update_user_password(self.test_user, "new_hashed_password", self.mock_db)
        self.assertEqual(self.test_user.password, "new_hashed_password")
        self.mock_db.commit.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()