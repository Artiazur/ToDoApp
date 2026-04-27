from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime


class RefreshTokenModel(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    exp: Mapped[datetime] = mapped_column()
    user: Mapped["UserModel"] = relationship(
        back_populates="refresh_token", uselist=False)
