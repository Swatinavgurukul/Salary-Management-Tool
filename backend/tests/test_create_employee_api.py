"""TDD Step 3 — POST /employees API tests.

RED phase: endpoint does not exist yet, so all tests will 404/fail.
"""
import pytest


VALID_EMPLOYEE = {
    "full_name": "Priya Sharma",
    "job_title": "Data Analyst",
    "country": "India",
    "salary": 72000.0,
    "department": "Analytics",
    "email": "priya.sharma@example.com",
}


class TestCreateEmployeeSuccess:

    def test_returns_201_on_valid_payload(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE)
        assert response.status_code == 201

    def test_response_contains_generated_id(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE)
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_response_echoes_back_all_fields(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE)
        data = response.json()
        assert data["full_name"] == "Priya Sharma"
        assert data["job_title"] == "Data Analyst"
        assert data["country"] == "India"
        assert data["salary"] == 72000.0
        assert data["department"] == "Analytics"
        assert data["email"] == "priya.sharma@example.com"

    def test_employee_persisted_in_database(self, client, db_session):
        client.post("/employees", json=VALID_EMPLOYEE)

        from app.models import Employee
        count = db_session.query(Employee).count()
        assert count == 1

    def test_created_at_is_populated(self, client):
        response = client.post("/employees", json=VALID_EMPLOYEE)
        data = response.json()
        assert data["created_at"] is not None


class TestCreateEmployeeSalaryValidation:

    def test_negative_salary_returns_422(self, client):
        payload = {**VALID_EMPLOYEE, "salary": -5000}
        response = client.post("/employees", json=payload)
        assert response.status_code == 422

    def test_zero_salary_returns_422(self, client):
        payload = {**VALID_EMPLOYEE, "salary": 0}
        response = client.post("/employees", json=payload)
        assert response.status_code == 422

    def test_error_body_mentions_salary(self, client):
        payload = {**VALID_EMPLOYEE, "salary": -1}
        response = client.post("/employees", json=payload)
        body = response.text.lower()
        assert "salary" in body


class TestCreateEmployeeMissingFields:

    @pytest.mark.parametrize("missing_field", [
        "full_name", "job_title", "country", "salary", "department", "email",
    ])
    def test_missing_required_field_returns_422(self, client, missing_field):
        payload = {k: v for k, v in VALID_EMPLOYEE.items() if k != missing_field}
        response = client.post("/employees", json=payload)
        assert response.status_code == 422

    def test_empty_name_returns_422(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": ""}
        response = client.post("/employees", json=payload)
        assert response.status_code == 422

    def test_duplicate_email_returns_409(self, client):
        client.post("/employees", json=VALID_EMPLOYEE)
        response = client.post("/employees", json=VALID_EMPLOYEE)
        assert response.status_code == 409
