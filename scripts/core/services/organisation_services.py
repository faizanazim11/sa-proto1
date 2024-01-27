from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import any_, exists, func
from sqlmodel import Session, select

from scripts.core.schemas.pg_models import ListingResponse, OrganizationDetails, OrganizationListingFilters, engine
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
    count_query = None
    where_conditions = []
    if filters:
        if filters.name:
            where_conditions.append(OrganizationDetails.name.ilike(f"%{filters.name.lower()}%"))
        if filters.city:
            where_conditions.append(OrganizationDetails.city.ilike(any_(filters.city)))
        if filters.state:
            where_conditions.append(OrganizationDetails.state.ilike(any_(filters.state)))
        if filters.pincode:
            where_conditions.append(OrganizationDetails.pincode.in_(filters.pincode))
        if filters.sector:
            column_valued = func.unnest(OrganizationDetails.sector).column_valued()
            where_conditions.append(exists(select(column_valued).where(column_valued.ilike(any_(filters.sector)))))
        query = query.where(*where_conditions)
        if filters.limit:
            count_query = select(func.count()).select_from(OrganizationDetails).order_by(None).where(*where_conditions)
            query = query.offset((filters.page - 1) * filters.limit).limit(filters.limit)
    with Session(engine) as session:
        count = session.exec(count_query).first() if count_query is not None else None
        results = jsonable_encoder(session.exec(query).all())
        return ListingResponse(
            data=results,
            total_records=count,
            end_of_records=(count <= (filters.page * filters.limit) if count else True),
        )


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
