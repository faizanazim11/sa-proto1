from typing import List, Optional

from pydantic import field_validator
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
    posted_by: Optional[int] = Field(default=None, foreign_key="organization_details.id", index=True)


engine = create_engine(Databases.POSTGRES_URI, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine, checkfirst=True)
