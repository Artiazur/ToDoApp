from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped["TaskModel"] = relationship(back_populates="user")
    refresh_token: Mapped["RefreshTokenModel"] = relationship(
        back_populates="user", uselist=False)
