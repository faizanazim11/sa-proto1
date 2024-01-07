from typing import Optional

from pydantic import field_validator
from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel

from scripts.config import Databases


class OrganizationDetails(SQLModel, table=True):
    __tablename__ = "organization_details"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str
    pincode: int = Field(index=True)
    sector: str = Field(index=True)
    profile: Optional[str] = None


class OrganizationListingFilters(SQLModel):
    name: Optional[str] = None
    location: Optional[list[str]] = None
    pincode: Optional[list[int]] = None
    sector: Optional[list[str]] = None

    @field_validator("location", "sector", mode="before")
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
