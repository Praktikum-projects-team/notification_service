import logging

import backoff
import sqlalchemy
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from core.config import pg_config

# from sqlalchemy.orm import sessionmaker
# from db.models_pg import Base
#
# engine = create_engine(pg_config.url, echo=True)
# Base.metadata.create_all(engine)
#
# Session = sessionmaker(bind=engine)
# session = Session()


class PostgresConnector:
    def __init__(self):
        self.pg_config = pg_config
        self.session = None
        self.engine = None
        self.conn = None

    @backoff.on_exception(backoff.expo, sqlalchemy.exc.OperationalError)
    def connect(self):
        if not self.engine:
            self.engine = create_engine(self.pg_config.url, echo=False)
        if not self.conn:
            logging.info("Connect db")
            self.conn = self.engine.connect()
        if not self.session:
            self.session = Session(bind=self.engine)
        self.__check_connect()

    def __check_connect(self):
        self.conn.scalar(select(1))
