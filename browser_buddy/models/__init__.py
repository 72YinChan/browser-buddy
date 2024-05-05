from datetime import datetime
from typing import Optional

from typing_extensions import Annotated
from sqlalchemy import create_engine, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, scoped_session


database_uri = 'sqlite+pysqlite:///F:/Projects/browser-buddy/browser_buddy/browser_buddy.db'
engine = create_engine(database_uri, echo=True)
Session = scoped_session(sessionmaker(engine))


int_pk = Annotated[int, mapped_column(primary_key=True)]
str_1000 = Annotated[str, mapped_column(String(1000), server_default='')]
str_255 = Annotated[str, mapped_column(String(255), server_default='')]
text = Annotated[str, mapped_column(Text, server_default='')]


class Base(DeclarativeBase):
    ...


class DateTimeMixin:

    # sqlite3
    create_date: Mapped[Optional[datetime]] = mapped_column(insert_default=datetime.now)
    update_date: Mapped[Optional[datetime]] = mapped_column(insert_default=datetime.now, onupdate=datetime.now)
