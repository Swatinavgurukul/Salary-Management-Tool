from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee_service import (
    create, get_by_id, list_paginated, update, delete,
    DuplicateEmailError, EmployeeNotFoundError,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return create(db, payload)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An employee with this email already exists.",
        )


@router.get("")
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return list_paginated(db, page, page_size, search)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        return get_by_id(db, employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found")


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update(db, employee_id, payload)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found")
    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An employee with this email already exists.",
        )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        delete(db, employee_id)
    except EmployeeNotFoundError:
        raise HTTPException(status_code=404, detail="Employee not found")
