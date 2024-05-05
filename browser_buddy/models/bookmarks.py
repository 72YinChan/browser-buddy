from sqlalchemy.orm import Mapped

from models import Base, DateTimeMixin, engine
from models import int_pk, str_1000, str_255, text


class Bookmarks(Base, DateTimeMixin):

    __tablename__ = 'bookmarks'

    id: Mapped[int_pk]
    url: Mapped[str_1000]
    name: Mapped[str_255]
    content: Mapped[text]
    date_added: Mapped[str_255]
    date_last_used: Mapped[str_255]

    def __repr__(self):
        url = self.url if len(self.url) <= 25 else self.url[:21] + ' ...'
        name = self.name if len(self.name) <= 25 else self.name[:21] + ' ...'
        return f"<BookMark(url={url}, name={name})>"


if __name__ == '__main__':
    Base.metadata.create_all(engine)
