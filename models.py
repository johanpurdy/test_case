from sqlalchemy import create_engine, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class DataAmperage(Base):
    __tablename__ = 'data_amperage'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    U1: Mapped[int] = mapped_column(Integer, nullable=False)
    U2: Mapped[int] = mapped_column(Integer, nullable=False)
    U3: Mapped[int] = mapped_column(Integer, nullable=False)
    I1: Mapped[int] = mapped_column(Integer, nullable=False)
    I2: Mapped[int] = mapped_column(Integer, nullable=False)
    I3: Mapped[int] = mapped_column(Integer, nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)


engine = create_engine("mysql+pymysql://root:root1234@localhost/measurements")
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Таблицы созданы")
