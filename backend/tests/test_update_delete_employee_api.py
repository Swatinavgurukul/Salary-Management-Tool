"""TDD Step 4b — PUT /employees/{id} and DELETE /employees/{id} tests.

RED phase: endpoints do not exist yet, so all tests will fail.
"""
import pytest


EMPLOYEE = {
    "full_name": "Carlos Ruiz",
    "job_title": "Manager",
    "country": "Spain",
    "salary": 95000,
    "department": "Operations",
    "email": "carlos@example.com",
}


class TestUpdateEmployee:

    def _create(self, client):
        resp = client.post("/employees", json=EMPLOYEE)
        return resp.json()["id"]

    def test_returns_200_on_valid_update(self, client):
        emp_id = self._create(client)
        response = client.put(f"/employees/{emp_id}", json={"salary": 100000})
        assert response.status_code == 200

    def test_updates_single_field(self, client):
        emp_id = self._create(client)
        client.put(f"/employees/{emp_id}", json={"salary": 110000})

        data = client.get(f"/employees/{emp_id}").json()
        assert data["salary"] == 110000
        assert data["full_name"] == "Carlos Ruiz"  # unchanged

    def test_updates_multiple_fields(self, client):
        emp_id = self._create(client)
        client.put(f"/employees/{emp_id}", json={
            "job_title": "Director",
            "country": "Portugal",
        })

        data = client.get(f"/employees/{emp_id}").json()
        assert data["job_title"] == "Director"
        assert data["country"] == "Portugal"

    def test_returns_404_for_nonexistent_employee(self, client):
        response = client.put("/employees/99999", json={"salary": 50000})
        assert response.status_code == 404

    def test_negative_salary_update_returns_422(self, client):
        emp_id = self._create(client)
        response = client.put(f"/employees/{emp_id}", json={"salary": -500})
        assert response.status_code == 422

    def test_empty_name_update_returns_422(self, client):
        emp_id = self._create(client)
        response = client.put(f"/employees/{emp_id}", json={"full_name": ""})
        assert response.status_code == 422

    def test_duplicate_email_update_returns_409(self, client):
        self._create(client)
        other = {**EMPLOYEE, "full_name": "Other", "email": "other@example.com"}
        resp2 = client.post("/employees", json=other)
        other_id = resp2.json()["id"]

        response = client.put(
            f"/employees/{other_id}", json={"email": "carlos@example.com"}
        )
        assert response.status_code == 409


class TestDeleteEmployee:

    def _create(self, client):
        resp = client.post("/employees", json=EMPLOYEE)
        return resp.json()["id"]

    def test_returns_204_on_successful_delete(self, client):
        emp_id = self._create(client)
        response = client.delete(f"/employees/{emp_id}")
        assert response.status_code == 204

    def test_employee_removed_from_database(self, client):
        emp_id = self._create(client)
        client.delete(f"/employees/{emp_id}")

        response = client.get(f"/employees/{emp_id}")
        assert response.status_code == 404

    def test_returns_404_for_nonexistent_employee(self, client):
        response = client.delete("/employees/99999")
        assert response.status_code == 404

    def test_delete_is_idempotent_404_on_second_call(self, client):
        emp_id = self._create(client)
        client.delete(f"/employees/{emp_id}")
        response = client.delete(f"/employees/{emp_id}")
        assert response.status_code == 404
