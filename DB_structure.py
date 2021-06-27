from sqlalchemy import Float, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TradeDetail(Base):
    __tablename__ = 'TradeDetail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_num = Column(String, nullable=False)
    brokerage_name = Column(String, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    total = Column(Float, nullable=False)
    buy_avg = Column(Float, nullable=False)
    buy_quantity = Column(Integer, nullable=False)
    sell_avg = Column(Float, nullable=False)
    sell_quantity = Column(Integer, nullable=False)


class TraceList(Base):
    __tablename__ = 'TraceList'
    stock_num = Column(String, primary_key=True, nullable=False)
    stock_name = Column(String, nullable=False)

def create(engine):
    Base.metadata.create_all(engine)
