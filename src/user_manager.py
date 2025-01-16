import uuid
from datetime import datetime
from typing import Optional

class UserManager:
    def __init__(self):
        self.users = {}
        
    def create_user(self) -> str:
        user_id = str(uuid.uuid4())
        self.users[user_id] = {
            'created_at': datetime.now()
        }
        return user_id
        
    def user_exists(self, user_id: str) -> bool:
        return user_id in self.users