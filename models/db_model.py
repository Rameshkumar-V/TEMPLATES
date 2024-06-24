from sqlalchemy import (Column , Integer, String, Boolean, DateTime, ForeignKey, text)

# DATABASE
from database.database import Base

Base = Base


class CollectionDetail(Base):
    __tablename__ = 'collection_details'

    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    column_name = Column(String, nullable=False, unique=True)
    label = Column(String, nullable=False)
    column_type = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    is_required = Column(Boolean, default=False)
    max_length = Column(Integer)
    min_length = Column(Integer)
    no_precision = Column(Integer)
    default_value = Column(String)
    is_unique = Column(Boolean, default=False)
    foreign_table_name = Column(String)
    foreign_column_name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    validation_regex = Column(String)
    error_msg = Column(String)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String)
    age = Column(Integer)

class Reports(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tablename =  Column(String, nullable=False)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    elapse_time = Column(String, nullable=False)
    upload_is_success = Column(Boolean, nullable=False)
    total_no_of_records = Column(Integer, nullable=False)
    uploaded_records = Column(Integer, nullable=False)
    un_uploaded_records = Column(Integer, nullable=False)
