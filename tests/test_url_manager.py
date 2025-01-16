import pytest
from datetime import datetime, timedelta
from src.url_manager import URLManager
import time

@pytest.fixture
def url_manager():
    config = {
        "url_length": 6,
        "default_lifetime": 24,
        "default_visits": 100,
        "min_visits": 1,
        "max_visits": 1000
    }
    return URLManager(config)

def test_create_url(url_manager):
    short_url = url_manager.create_url("https://example.com", "user123")
    assert len(short_url) == url_manager.config["url_length"]
    assert short_url in url_manager.urls

def test_get_url(url_manager):
    short_url = url_manager.create_url("https://example.com", "user123")
    original_url = url_manager.get_url(short_url)
    assert original_url == "https://example.com"

def test_delete_url(url_manager):
    short_url = url_manager.create_url("https://example.com", "user123")
    result = url_manager.delete_url(short_url, "user123")
    assert result is True
    assert short_url not in url_manager.urls

def test_edit_url(url_manager):
    short_url = url_manager.create_url("https://example.com", "user123")
    new_limit = 200
    result = url_manager.edit_url(short_url, "user123", new_limit)
    assert result is True
    assert url_manager.urls[short_url]['visits_limit'] == new_limit

def test_cleanup_expired(url_manager):
    short_url = url_manager.create_url("https://example.com", "user123", lifetime_hours=0.0001)
    assert short_url in url_manager.urls
    time.sleep(1)  # Задержка, чтобы дать время истечь
    url_manager.cleanup_expired()
    assert short_url not in url_manager.urls

def test_visits_limit(url_manager):
    short_url = url_manager.create_url("https://example.com", "user123", visits_limit=1)
    url_manager.get_url(short_url)  # First visit
    original_url = url_manager.get_url(short_url)  # Second visit should fail
    assert original_url is None