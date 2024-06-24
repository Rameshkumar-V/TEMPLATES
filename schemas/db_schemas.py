from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import date

class CollectionDetailBase(BaseModel):
    table_name: str = Field(..., example="table_name")
    column_name: str = Field(..., example="example_column")
    label: str = Field(..., example="Label for show")
    column_type: str = Field(..., example="String")
    status: bool = Field(default=True)
    is_required: bool = Field(default=False)
    max_length: Optional[int] = Field(None, example=255)
    min_length: Optional[int] = Field(None, example=0)
    no_precision: Optional[int] = Field(None, example=2)
    default_value: Optional[str] = Field(None, example="default")
    is_unique: bool = Field(default=False)
    foreign_table_name: Optional[str] = Field(None, example="foreign_table")
    foreign_column_name: Optional[str] = Field(None, example="foreign_column")
    description: Optional[str] = Field(None, example="Description of the column")
    validation_regex: Optional[str] = Field(None, example="^[a-zA-Z0-9]+$")
    error_msg : str = Field(..., example="Error Message")

class CollectionDetailCreate(CollectionDetailBase):
    pass

class CollectionDetailUpdate(CollectionDetailBase):
    id: int

class CollectionDetail(CollectionDetailBase):
    id: int

    class Config:
        orm_mode: True


class UserBase(BaseModel):
    name: str = Field(..., example="username")
    password: str = Field(..., example="password")
    email: Optional[EmailStr] = Field(None, example="user@example.com")
    age: int
