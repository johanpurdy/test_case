from sqlalchemy import create_engine, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class DataAmperage(Base):
    __tablename__ = 'data_amperage'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    U1: Mapped[int] = mapped_column(Integer, nullable=True)
    U2: Mapped[int] = mapped_column(Integer, nullable=True)
    U3: Mapped[int] = mapped_column(Integer, nullable=True)
    I1: Mapped[int] = mapped_column(Integer, nullable=True)
    I2: Mapped[int] = mapped_column(Integer, nullable=True)
    I3: Mapped[int] = mapped_column(Integer, nullable=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)


engine = create_engine("mysql+pymysql://root:123456@localhost/my_measurements")
Base.metadata.create_all(engine)
