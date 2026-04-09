"""TDD Step 4a — GET /employees API tests (updated for paginated response)."""

EMPLOYEE_1 = {
    "full_name": "Alice Smith",
    "job_title": "Engineer",
    "country": "India",
    "salary": 80000,
    "department": "Engineering",
    "email": "alice@example.com",
}

EMPLOYEE_2 = {
    "full_name": "Bob Jones",
    "job_title": "Designer",
    "country": "US",
    "salary": 90000,
    "department": "Design",
    "email": "bob@example.com",
}


class TestGetEmployeesList:

    def test_returns_200(self, client):
        response = client.get("/employees")
        assert response.status_code == 200

    def test_returns_empty_list_when_no_employees(self, client):
        data = client.get("/employees").json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_returns_all_employees(self, client):
        client.post("/employees", json=EMPLOYEE_1)
        client.post("/employees", json=EMPLOYEE_2)

        data = client.get("/employees").json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_each_employee_has_required_fields(self, client):
        client.post("/employees", json=EMPLOYEE_1)

        data = client.get("/employees").json()
        emp = data["items"][0]
        for field in ("id", "full_name", "job_title", "country", "salary",
                       "department", "email"):
            assert field in emp


class TestGetSingleEmployee:

    def test_returns_200_for_existing_employee(self, client):
        create_resp = client.post("/employees", json=EMPLOYEE_1)
        emp_id = create_resp.json()["id"]

        response = client.get(f"/employees/{emp_id}")
        assert response.status_code == 200

    def test_returns_correct_employee_by_id(self, client):
        create_resp = client.post("/employees", json=EMPLOYEE_1)
        emp_id = create_resp.json()["id"]

        response = client.get(f"/employees/{emp_id}")
        data = response.json()
        assert data["full_name"] == "Alice Smith"
        assert data["email"] == "alice@example.com"

    def test_returns_404_for_nonexistent_employee(self, client):
        response = client.get("/employees/99999")
        assert response.status_code == 404
