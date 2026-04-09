from typing import Optional, List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models import Employee


def _aggregate(query):
    """Run MIN/MAX/AVG/COUNT on a filtered query. Returns None if empty."""
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


def country_stats(db: Session, country: str) -> Optional[dict]:
    query = db.query(Employee).filter(
        func.lower(Employee.country) == country.lower()
    )
    result = _aggregate(query)
    if result:
        result["country"] = country
    return result


def job_title_stats(
    db: Session, job_title: str, country: Optional[str] = None
) -> Optional[dict]:
    query = db.query(Employee).filter(
        func.lower(Employee.job_title) == job_title.lower()
    )
    if country:
        query = query.filter(func.lower(Employee.country) == country.lower())

    result = _aggregate(query)
    if result:
        result["job_title"] = job_title
        if country:
            result["country"] = country
    return result


def department_breakdown(db: Session) -> List[dict]:
    rows = (
        db.query(
            Employee.department,
            func.count(Employee.id).label("employee_count"),
            func.min(Employee.salary).label("min_salary"),
            func.max(Employee.salary).label("max_salary"),
            func.avg(Employee.salary).label("avg_salary"),
        )
        .group_by(Employee.department)
        .order_by(desc("employee_count"))
        .all()
    )
    return [
        {
            "department": r.department,
            "employee_count": r.employee_count,
            "min_salary": r.min_salary,
            "max_salary": r.max_salary,
            "avg_salary": round(r.avg_salary, 2),
        }
        for r in rows
    ]


def headcount_by_country(db: Session) -> List[dict]:
    rows = (
        db.query(
            Employee.country,
            func.count(Employee.id).label("employee_count"),
            func.avg(Employee.salary).label("avg_salary"),
        )
        .group_by(Employee.country)
        .order_by(desc("employee_count"))
        .all()
    )
    return [
        {
            "country": r.country,
            "employee_count": r.employee_count,
            "avg_salary": round(r.avg_salary, 2),
        }
        for r in rows
    ]


def top_earners(db: Session, limit: int = 10) -> List[Employee]:
    return (
        db.query(Employee)
        .order_by(desc(Employee.salary))
        .limit(limit)
        .all()
    )
