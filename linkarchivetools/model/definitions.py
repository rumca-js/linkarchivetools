from typing import Optional
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    select,
    func,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    delete,
    update,
    asc,
    desc,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import timedelta, datetime, timezone

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


Base = declarative_base()


class ApiKeys(Base):
    __tablename__ = "apikeys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(1000), unique=True)
    user_id: Mapped[int]


class Keywords(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword: Mapped[str] = mapped_column(String(200), unique=True)
    language: Mapped[str] = mapped_column(String(10))
    user_id: Mapped[int]


def create_tables(engine):
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
