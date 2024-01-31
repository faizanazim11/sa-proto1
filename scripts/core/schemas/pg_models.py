import re
from typing import List, Optional

from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine
from sqlmodel import ARRAY, Column, Field, SQLModel, String

from scripts.config import Databases


class OrganizationDetails(SQLModel, table=True):
    __tablename__ = "organization_details"
    id: Optional[int] = Field(default=None, primary_key=True)
    pincode: int = Field(index=True)
    registered_year: Optional[int] = None
    name: str = Field(index=True)
    city: str = Field(index=True)
    state: str = Field(index=True)
    sector: List[str] = Field(sa_column=Column(ARRAY(String, dimensions=1), default=[]))
    employee_count: Optional[str] = None
    logo: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    profile: Optional[str] = None


class OrganizationListingFilters(SQLModel):
    name: Optional[str] = None
    city: Optional[list[str]] = None
    state: Optional[list[str]] = None
    pincode: Optional[list[int]] = None
    sector: Optional[list[str]] = None
    page: Optional[int] = 1
    limit: Optional[int] = None

    @field_validator("city", "state", "sector", mode="before")
    @classmethod
    def lower_values(cls, values):
        if values:
            values = [f"%{value.lower()}%" for value in values]
        return values


class JobDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    qualification: str
    salary: Optional[str] = Field(default=None, index=True)
    posted_by: int = Field(foreign_key="organization_details.id", index=True)


class JobListingFilters(SQLModel):
    title: Optional[str] = None
    posted_by: Optional[List[int]] = None
    sector: Optional[List[str]] = None
    city: Optional[List[str]] = None
    state: Optional[List[str]] = None
    pincode: Optional[List[int]] = None
    page: Optional[int] = 1
    limit: Optional[int] = None

    @field_validator("city", "state", "sector", mode="before")
    @classmethod
    def lower_values(cls, values):
        if values:
            values = [f"%{value.lower()}%" for value in values]
        return values

    @field_validator("title", mode="before")
    @classmethod
    def break_title(cls, values):
        if values:
            values = "%".join(re.split(r',|-', values))
        return values


class JobSearchFilters(BaseModel):
    query: str
    location: Optional[str] = None
    page: Optional[int] = 1
    limit: Optional[int] = None


class ListingResponse(BaseModel):
    data: Optional[list[dict]] = None
    end_of_records: Optional[bool] = False
    total_records: Optional[int] = None


engine = create_engine(Databases.POSTGRES_URI, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine, checkfirst=True)
