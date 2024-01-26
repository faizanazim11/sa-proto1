from fastapi import APIRouter
from sqlalchemy import any_, exists, func
from sqlmodel import Session, select

from scripts.core.schemas.pg_models import JobDetails, JobListingFilters, OrganizationDetails, engine

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
    if filters:
        if filters.title:
            query = query.where(JobDetails.title.ilike(f"%{filters.title.lower()}%"))
        if filters.posted_by:
            query = query.where(JobDetails.posted_by.in_(filters.posted_by))
        if filters.sector:
            column_valued = func.unnest(OrganizationDetails.sector).column_valued()
            query = query.where(exists(select(column_valued).where(column_valued.ilike(any_(filters.sector)))))
        if filters.city:
            query = query.where(OrganizationDetails.city.ilike(any_(filters.city)))
        if filters.state:
            query = query.where(OrganizationDetails.state.ilike(any_(filters.state)))
        if filters.pincode:
            query = query.where(OrganizationDetails.pincode.in_(filters.pincode))
    with Session(engine) as session:
        return session.exec(query).mappings().all()


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
