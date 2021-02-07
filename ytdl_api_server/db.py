import attr

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
import os

Base = declarative_base()


class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    timestamp_added = Column(Date, nullable=False)
    timestamp_downloaded = Column(Date, nullable=True, default=None)

    def __repr__(self):
        return f"<Url(url='{self.url}' added at {self.timestamp_added}, downloaded at {self.timestamp_downloaded}"


@attr.s
class DB:
    sqlite_filename = attr.ib(default=os.getenv("DB_FILE_PATH", "db.sqlite3"))
    debug = attr.ib(default=False)

    def __attrs_post_init__(self):
        self.engine = create_engine(
            f"sqlite:///{self.sqlite_filename}", echo=self.debug
        )
        Base.metadata.create_all(self.engine)
        self.session_base = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session_base()

    def add_url(self, url):
        session = self.get_session()
        u = Url(url=url, timestamp_added=datetime.now())
        session.add(u)
        session.commit()

    def get_pending_urls(self):
        session = self.get_session()
        return {
            url.id: url.url
            for url in session.query(Url)
            .filter_by(timestamp_downloaded=None)
            .all()
        }

    def mark_url_downloaded(self, urlid):
        session = self.get_session()
        urlq = session.query(Url).filter_by(id=urlid).first()
        urlq.timestamp_downloaded = datetime.now()
        session.commit()

if __name__ == "__main__":
    db = DB()
    db.add_url("foo")
    db.add_url("bar")
    print(db.get_pending_urls())
