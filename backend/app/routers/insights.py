from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmployeeResponse
from app.services import insight_service

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/country/{country}")
def country_insights(country: str, db: Session = Depends(get_db)):
    result = insight_service.country_stats(db, country)
    if result is None:
        raise HTTPException(status_code=404, detail="No employees found for this country")
    return result


@router.get("/job")
def job_insights(
    job_title: str = Query(..., min_length=1),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    result = insight_service.job_title_stats(db, job_title, country)
    if result is None:
        raise HTTPException(status_code=404, detail="No employees found for this filter")
    return result


@router.get("/department")
def department_insights(db: Session = Depends(get_db)):
    return insight_service.department_breakdown(db)


@router.get("/headcount")
def headcount(db: Session = Depends(get_db)):
    return insight_service.headcount_by_country(db)


@router.get("/top-earners", response_model=List[EmployeeResponse])
def top_earners(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return insight_service.top_earners(db, limit)
