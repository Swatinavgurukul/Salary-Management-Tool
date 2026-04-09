from typing import Optional

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse


class DuplicateEmailError(Exception):
    pass


class EmployeeNotFoundError(Exception):
    pass


def create(db: Session, payload: EmployeeCreate) -> Employee:
    employee = Employee(**payload.model_dump())
    db.add(employee)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError()
    db.refresh(employee)
    return employee


def get_by_id(db: Session, employee_id: int) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise EmployeeNotFoundError()
    return employee


def list_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
) -> dict:
    query = db.query(Employee)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Employee.full_name.ilike(pattern),
                Employee.job_title.ilike(pattern),
                Employee.country.ilike(pattern),
                Employee.department.ilike(pattern),
                Employee.email.ilike(pattern),
            )
        )

    total = query.count()
    items = (
        query.order_by(Employee.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": [EmployeeResponse.model_validate(emp) for emp in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def update(db: Session, employee_id: int, payload: EmployeeUpdate) -> Employee:
    employee = get_by_id(db, employee_id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError()
    db.refresh(employee)
    return employee


def delete(db: Session, employee_id: int) -> None:
    employee = get_by_id(db, employee_id)
    db.delete(employee)
    db.commit()
