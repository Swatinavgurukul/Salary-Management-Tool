"""TDD Step 2 — Employee Model tests.

RED phase: these tests define the contract for Employee validation.
Several will FAIL until the model and schema enforce the rules.
"""
import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Employee
from app.schemas import EmployeeCreate


# ── Valid creation ──────────────────────────────────────────────

class TestValidEmployeeCreation:

    def test_create_employee_with_all_fields(self, db_session):
        emp = Employee(
            full_name="Alice Smith",
            job_title="Software Engineer",
            country="India",
            salary=85000.0,
            department="Engineering",
            email="alice.smith@example.com",
        )
        db_session.add(emp)
        db_session.commit()
        db_session.refresh(emp)

        assert emp.id is not None
        assert emp.full_name == "Alice Smith"
        assert emp.job_title == "Software Engineer"
        assert emp.country == "India"
        assert emp.salary == 85000.0
        assert emp.department == "Engineering"
        assert emp.email == "alice.smith@example.com"

    def test_auto_generated_id_is_unique(self, db_session):
        emp1 = Employee(full_name="A", job_title="Dev", country="US",
                        salary=1000, department="Eng", email="a@x.com")
        emp2 = Employee(full_name="B", job_title="Dev", country="US",
                        salary=2000, department="Eng", email="b@x.com")
        db_session.add_all([emp1, emp2])
        db_session.commit()

        assert emp1.id != emp2.id

    def test_created_at_is_set_automatically(self, db_session):
        emp = Employee(full_name="Ts", job_title="QA", country="UK",
                       salary=5000, department="QA", email="ts@x.com")
        db_session.add(emp)
        db_session.commit()
        db_session.refresh(emp)

        assert emp.created_at is not None


# ── Salary validation ──────────────────────────────────────────

class TestSalaryValidation:

    def test_negative_salary_rejected_by_schema(self):
        """Schema must reject salary < 0."""
        with pytest.raises(Exception):
            EmployeeCreate(
                full_name="Bad Salary",
                job_title="Dev",
                country="US",
                salary=-5000.0,
                department="Eng",
                email="neg@x.com",
            )

    def test_zero_salary_rejected_by_schema(self):
        """Schema must reject salary == 0."""
        with pytest.raises(Exception):
            EmployeeCreate(
                full_name="Zero Salary",
                job_title="Dev",
                country="US",
                salary=0,
                department="Eng",
                email="zero@x.com",
            )

    def test_negative_salary_rejected_at_db_level(self, db_session):
        """DB constraint must prevent negative salary from being persisted."""
        emp = Employee(full_name="Bad", job_title="Dev", country="US",
                       salary=-100, department="Eng", email="bad@x.com")
        db_session.add(emp)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_positive_salary_accepted(self):
        """Schema must accept a valid positive salary."""
        emp = EmployeeCreate(
            full_name="Good Salary",
            job_title="Dev",
            country="US",
            salary=75000.0,
            department="Eng",
            email="good@x.com",
        )
        assert emp.salary == 75000.0


# ── Required-field validation ──────────────────────────────────

class TestRequiredFields:

    def test_name_is_required_by_schema(self):
        """Omitting full_name must raise a validation error."""
        with pytest.raises(Exception):
            EmployeeCreate(
                job_title="Dev",
                country="US",
                salary=50000,
                department="Eng",
                email="no-name@x.com",
            )

    def test_empty_name_rejected_by_schema(self):
        """Empty string for full_name must be rejected."""
        with pytest.raises(Exception):
            EmployeeCreate(
                full_name="",
                job_title="Dev",
                country="US",
                salary=50000,
                department="Eng",
                email="empty@x.com",
            )

    def test_job_title_is_required_by_schema(self):
        with pytest.raises(Exception):
            EmployeeCreate(
                full_name="No Title",
                country="US",
                salary=50000,
                department="Eng",
                email="notitle@x.com",
            )

    def test_country_is_required_by_schema(self):
        with pytest.raises(Exception):
            EmployeeCreate(
                full_name="No Country",
                job_title="Dev",
                salary=50000,
                department="Eng",
                email="nocountry@x.com",
            )

    def test_name_required_at_db_level(self, db_session):
        """DB NOT NULL constraint must reject a null full_name."""
        emp = Employee(full_name=None, job_title="Dev", country="US",
                       salary=5000, department="Eng", email="null@x.com")
        db_session.add(emp)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_email_must_be_unique(self, db_session):
        """Duplicate emails must be rejected by DB unique constraint."""
        emp1 = Employee(full_name="A", job_title="Dev", country="US",
                        salary=1000, department="Eng", email="dup@x.com")
        emp2 = Employee(full_name="B", job_title="Dev", country="US",
                        salary=2000, department="Eng", email="dup@x.com")
        db_session.add(emp1)
        db_session.commit()
        db_session.add(emp2)
        with pytest.raises(IntegrityError):
            db_session.commit()
