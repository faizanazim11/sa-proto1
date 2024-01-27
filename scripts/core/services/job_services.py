from fastapi import APIRouter
from sqlalchemy import any_, exists, func
from sqlmodel import Session, select

from scripts.core.handlers.ai_convo_handler import get_filter_json
from scripts.core.schemas.pg_models import (
    JobDetails,
    JobListingFilters,
    JobSearchFilters,
    ListingResponse,
    OrganizationDetails,
    engine,
)

job_services = APIRouter()


@job_services.post("/")
def create_job(job: JobDetails):
    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)
        return job


@job_services.get("/")
def get_job(filters: JobListingFilters = None):
    query = select(JobDetails.__table__.columns, OrganizationDetails.name).join(OrganizationDetails)
    count_query = None
    where_conditions = []
    if filters:
        if filters.title:
            where_conditions.append(JobDetails.title.ilike(f"%{filters.title.lower()}%"))
        if filters.posted_by:
            where_conditions.append(JobDetails.posted_by.in_(filters.posted_by))
        if filters.sector:
            column_valued = func.unnest(OrganizationDetails.sector).column_valued()
            where_conditions.append(exists(select(column_valued).where(column_valued.ilike(any_(filters.sector)))))
        if filters.city:
            where_conditions.append(OrganizationDetails.city.ilike(any_(filters.city)))
        if filters.state:
            where_conditions.append(OrganizationDetails.state.ilike(any_(filters.state)))
        if filters.pincode:
            where_conditions.append(OrganizationDetails.pincode.in_(filters.pincode))
        query = query.where(*where_conditions)
        if filters.limit:
            count_query = (
                select(func.count())
                .select_from(JobDetails)
                .join(OrganizationDetails)
                .with_only_columns(func.count())
                .order_by(None)
                .where(*where_conditions)
            )
            query = query.offset((filters.page - 1) * filters.limit).limit(filters.limit)
    with Session(engine) as session:
        count = session.exec(count_query).first() if count_query is not None else None
        results = session.exec(query).mappings().all()
        return ListingResponse(
            data=results,
            total_records=count,
            end_of_records=(count <= (filters.page * filters.limit) if count else True),
        )


@job_services.get("/{id}")
def get_job_by_id(id: int):
    with Session(engine) as session:
        return session.get(JobDetails, id)


@job_services.put("/{id}")
def update_job(id: int, job: JobDetails):
    with Session(engine) as session:
        job_obj = session.get(JobDetails, id)
        [setattr(job_obj, key, value) for key, value in job.model_dump(exclude_unset=True).items()]
        session.commit()
        session.refresh(job_obj)
        return job_obj


@job_services.get("/search/")
def search_job(search: JobSearchFilters):
    return get_job(
        JobListingFilters(**get_filter_json(search.query, search.location), page=search.page, limit=search.limit)
    )
