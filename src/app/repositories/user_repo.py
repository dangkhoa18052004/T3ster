from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import User

class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_email(self, email: str) -> bool:
        stmt = select(User.id).where(User.email == email)
        return self.db.execute(stmt).first() is not None

    def create(self, email: str, full_name: str) -> User:
        u = User(email=email, full_name=full_name)
        self.db.add(u)
        self.db.commit()
        self.db.refresh(u)
        return u

    def get(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)
