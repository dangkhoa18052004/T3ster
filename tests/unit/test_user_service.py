import pytest
from src.app.services.user_service import normalize_email, ensure_email_unique, DuplicateEmailError

class FakeRepo:
    def __init__(self, exists=False):
        self._exists = exists
    def exists_by_email(self, email: str) -> bool:
        return self._exists

def test_normalize_email():
    assert normalize_email("  A@B.COM ") == "a@b.com"

def test_ensure_email_unique_ok():
    repo = FakeRepo(exists=False)
    assert ensure_email_unique(" Demo@Example.com ", repo) == "demo@example.com"

def test_ensure_email_unique_duplicate():
    repo = FakeRepo(exists=True)
    with pytest.raises(DuplicateEmailError):
        ensure_email_unique("demo@example.com", repo)
