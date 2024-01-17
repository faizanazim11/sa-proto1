from fastapi import APIRouter
from sqlalchemy import any_, exists, func
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
            query = query.where(OrganizationDetails.name.ilike(f"%{filters.name.lower()}%"))
        if filters.city:
            query = query.where(OrganizationDetails.city.ilike(any_(filters.city)))
        if filters.state:
            query = query.where(OrganizationDetails.state.ilike(any_(filters.state)))
        if filters.pincode:
            query = query.where(OrganizationDetails.pincode.in_(filters.pincode))
        if filters.sector:
            column_valued = func.unnest(OrganizationDetails.sector).column_valued()
            query = query.where(exists(select(column_valued).where(column_valued.ilike(any_(filters.sector)))))
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
        [setattr(organisation_obj, key, value) for key, value in organisation.model_dump(exclude_unset=True).items()]
        session.commit()
        session.refresh(organisation_obj)
        return organisation_obj
