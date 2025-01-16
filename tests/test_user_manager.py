import pytest
from src.user_manager import UserManager

@pytest.fixture
def user_manager():
    return UserManager()

def test_create_user(user_manager):
    user_id = user_manager.create_user()
    assert user_manager.user_exists(user_id)

def test_user_exists(user_manager):
    user_id = user_manager.create_user()
    assert user_manager.user_exists(user_id)
    assert not user_manager.user_exists("non-existent-user")