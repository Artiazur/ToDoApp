from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime, timezone


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    # created_at: Mapped[datetime] = mapped_column(
    #     default=lambda: datetime.now(timezone.utc))
    # updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(
    #     timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user: Mapped["UserModel"] = relationship(
        back_populates="tasks", uselist=False)
