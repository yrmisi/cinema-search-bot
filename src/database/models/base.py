from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """ """

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now,
        nullable=False,
        sort_order=99,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Set the name of the table based on the class name in plural form."""
        return f"{cls.__name__.lower()}s"
