from ner import settings
from ner.db import DB
from sqlalchemy import Date, Column, String, JSON

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExtractedEntities(Base):
    __tablename__ = 'extracted_entities'
    __table_args__ = {'schema': settings.env}

    created_at = Column('created_at', Date)
    text = Column('text', String)
    entities = Column('entities', JSON)

engine = DB.create_engine()

# create schema if doesn't exist
if not engine.dialect.has_schema(engine, settings.env):
    engine.execute(schema.CreateSchema(settings.env))

Base.metadata.create_all(bind=engine)
