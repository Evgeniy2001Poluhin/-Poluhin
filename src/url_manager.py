from datetime import datetime, timedelta
import string
import random
import uuid
from typing import Optional, Dict, List

class URLManager:
    def __init__(self, config: dict):
        self.config = config
        self.urls: Dict[str, dict] = {}
        
    def generate_short_url(self, length: int = 6) -> str:
        """Генерирует короткую ссылку"""
        chars = string.ascii_letters + string.digits
        while True:
            short_url = ''.join(random.choice(chars) for _ in range(length))
            if short_url not in self.urls:
                return short_url

    def create_url(self, original_url: str, user_id: str, 
                  lifetime_hours: Optional[int] = None, 
                  visits_limit: Optional[int] = None) -> str:
        """Создает новую короткую ссылку"""
        short_url = self.generate_short_url(self.config['url_length'])
        
        if lifetime_hours is None or lifetime_hours > self.config['default_lifetime']:
            lifetime_hours = self.config['default_lifetime']
            
        if visits_limit is None:
            visits_limit = self.config['default_visits']
        elif visits_limit < self.config['min_visits']:
            visits_limit = self.config['min_visits']
        elif visits_limit > self.config['max_visits']:
            visits_limit = self.config['max_visits']

        self.urls[short_url] = {
            'original_url': original_url,
            'user_id': user_id,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=lifetime_hours),
            'visits_limit': visits_limit,
            'visits_count': 0,
            'is_active': True
        }
        
        return short_url

    def get_url(self, short_url: str) -> Optional[str]:
        """Получает оригинальный URL и увеличивает счетчик посещений"""
        if short_url not in self.urls:
            print("Ссылка не существует")
            return None
            
        url_data = self.urls[short_url]
        
        if not url_data['is_active']:
            print("Ссылка деактивирована")
            return None
            
        if datetime.now() > url_data['expires_at']:
            url_data['is_active'] = False
            print("Срок действия ссылки истек")
            return None
            
        if url_data['visits_count'] >= url_data['visits_limit']:
            url_data['is_active'] = False
            print("Достигнут лимит переходов по ссылке")
            return None
            
        url_data['visits_count'] += 1
        return url_data['original_url']

    def edit_url(self, short_url: str, user_id: str, new_visits_limit: int) -> bool:
        """Редактирует параметры ссылки"""
        if short_url not in self.urls:
            return False
            
        url_data = self.urls[short_url]
        if url_data['user_id'] != user_id:
            return False
            
        if new_visits_limit < self.config['min_visits']:
            new_visits_limit = self.config['min_visits']
        elif new_visits_limit > self.config['max_visits']:
            new_visits_limit = self.config['max_visits']
            
        url_data['visits_limit'] = new_visits_limit
        return True

    def delete_url(self, short_url: str, user_id: str) -> bool:
        """Удаляет ссылку"""
        if short_url not in self.urls:
            return False
            
        if self.urls[short_url]['user_id'] != user_id:
            return False
            
        del self.urls[short_url]
        return True

    def get_user_urls(self, user_id: str) -> List[dict]:
        """Получает список всех ссылок пользователя"""
        return [
            {
                'short_url': short_url,
                **url_data
            }
            for short_url, url_data in self.urls.items()
            if url_data['user_id'] == user_id
        ]

    def cleanup_expired(self) -> None:
        """Удаляет просроченные ссылки"""
        current_time = datetime.now()
        expired_urls = [
            short_url for short_url, data in self.urls.items()
            if current_time > data['expires_at'] or 
            data['visits_count'] >= data['visits_limit']
        ]
        for short_url in expired_urls:
            del self.urls[short_url]

    def console_redirect(self, short_url: str) -> None:
        """Осуществляет переход по короткой ссылке через консоль"""
        original_url = self.get_url(short_url)
        if original_url:
            print(f"Переход по ссылке: {original_url}")
        else:
            print("Ссылка недоступна или не существует")