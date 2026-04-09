from app.models import Employee
from app.database import Base


def test_employee_table_exists(db_session):
    """Verify the employees table is created in the database."""
    assert "employees" in Base.metadata.tables


def test_employee_model_columns():
    """Verify Employee model has all required columns."""
    columns = {col.name for col in Employee.__table__.columns}
    expected = {"id", "full_name", "job_title", "country", "salary",
                "department", "email", "created_at", "updated_at"}
    assert expected == columns


def test_create_employee_record(db_session):
    """Verify we can persist an Employee row and read it back."""
    emp = Employee(
        full_name="Jane Doe",
        job_title="Engineer",
        country="US",
        salary=95000.0,
        department="Engineering",
        email="jane.doe@example.com",
    )
    db_session.add(emp)
    db_session.commit()
    db_session.refresh(emp)

    assert emp.id is not None
    assert emp.full_name == "Jane Doe"
    assert emp.salary == 95000.0
