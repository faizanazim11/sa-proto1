from fastapi import APIRouter
from sqlalchemy import any_
from sqlmodel import Session, select

from scripts.core.schemas.pg_models import OrganizationDetails, OrganizationListingFilters, engine
from scripts.security import UserDetails

organisation_services = APIRouter()


@organisation_services.post("/")
def create_organisation(organisation: OrganizationDetails, _: UserDetails):
    with Session(engine) as session:
        session.add(organisation)
        session.commit()
        session.refresh(organisation)
        return organisation


@organisation_services.get("/")
def get_organisation(_: UserDetails, filters: OrganizationListingFilters = None):
    query = select(OrganizationDetails)
    if filters:
        if filters.name:
            query = query.where(OrganizationDetails.name.ilike(f"%{filters.name}%"))
        if filters.location:
            query = query.where(OrganizationDetails.location.ilike(any_(filters.location)))
        if filters.pincode:
            query = query.where(OrganizationDetails.pincode.in_(filters.pincode))
        if filters.sector:
            query = query.where(OrganizationDetails.sector.ilike(any_(filters.sector)))
    with Session(engine) as session:
        return session.exec(query).all()


@organisation_services.get("/{id}")
def get_organisation_by_id(id: int, _: UserDetails):
    with Session(engine) as session:
        return session.get(OrganizationDetails, id)


@organisation_services.put("/{id}")
def update_organisation(id: int, organisation: OrganizationDetails, _: UserDetails):
    with Session(engine) as session:
        organisation_obj = session.get(OrganizationDetails, id)
        organisation_obj.name = organisation.name
        organisation_obj.location = organisation.location
        organisation_obj.pincode = organisation.pincode
        organisation_obj.sector = organisation.sector
        organisation_obj.profile = organisation.profile
        session.commit()
        session.refresh(organisation_obj)
        return organisation_obj
