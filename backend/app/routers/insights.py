from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee

router = APIRouter(prefix="/insights", tags=["insights"])


def _aggregate(query):
    """Run MIN/MAX/AVG/COUNT on a filtered query and return a dict."""
    row = query.with_entities(
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.avg(Employee.salary).label("avg_salary"),
        func.count(Employee.id).label("employee_count"),
    ).first()

    if row.employee_count == 0:
        return None

    return {
        "min_salary": row.min_salary,
        "max_salary": row.max_salary,
        "avg_salary": round(row.avg_salary, 2),
        "employee_count": row.employee_count,
    }


@router.get("/country/{country}")
def country_insights(country: str, db: Session = Depends(get_db)):
    query = db.query(Employee).filter(
        func.lower(Employee.country) == country.lower()
    )
    result = _aggregate(query)
    if result is None:
        raise HTTPException(status_code=404, detail="No employees found for this country")
    result["country"] = country
    return result


@router.get("/job")
def job_insights(
    job_title: str = Query(..., min_length=1),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Employee).filter(
        func.lower(Employee.job_title) == job_title.lower()
    )
    if country:
        query = query.filter(func.lower(Employee.country) == country.lower())

    result = _aggregate(query)
    if result is None:
        raise HTTPException(status_code=404, detail="No employees found for this filter")
    result["job_title"] = job_title
    if country:
        result["country"] = country
    return result
