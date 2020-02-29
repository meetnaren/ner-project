from db import settings, DB
from sqlalchemy import DateTime, Column, String, schema, Float

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Triggers(Base):
    __tablename__ = 'Triggers'
    __table_args__ = {'schema': settings.env}

    id = Column('Id', String, primary_key=True, nullable=False)
    trigged_at = Column('trigged_at', DateTime)
    symbol = Column('stock_symbol', String)
    price = Column('price', Float)
    transaction_type = Column('transaction_type', String)


engine = DB.create_engine()

# create schema if doesn't exist
if not engine.dialect.has_schema(engine, settings.env):
    engine.execute(schema.CreateSchema(settings.env))

Base.metadata.create_all(bind=engine)
