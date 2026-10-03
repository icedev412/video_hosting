import hashlib

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


from datetime import datetime

from sqlalchemy import DateTime




class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user: Mapped["User"] = relationship()

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()