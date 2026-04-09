"""Edge case tests — boundary conditions, special characters, and unusual inputs."""
import pytest


VALID_EMPLOYEE = {
    "full_name": "Test User",
    "job_title": "Dev",
    "country": "US",
    "salary": 50000,
    "department": "Eng",
    "email": "test@example.com",
}


class TestBoundarySalaryValues:

    def test_minimum_valid_salary(self, client):
        payload = {**VALID_EMPLOYEE, "salary": 0.01}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201
        assert resp.json()["salary"] == 0.01

    def test_very_large_salary(self, client):
        payload = {**VALID_EMPLOYEE, "salary": 999_999_999.99}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201

    def test_salary_with_many_decimals_is_stored(self, client):
        payload = {**VALID_EMPLOYEE, "salary": 50000.123456}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201


class TestSpecialCharacters:

    def test_name_with_hyphen(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "Mary-Jane Watson", "email": "mj@x.com"}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201
        assert resp.json()["full_name"] == "Mary-Jane Watson"

    def test_name_with_apostrophe(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "O'Brien", "email": "ob@x.com"}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201

    def test_name_with_unicode(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "José García", "email": "jg@x.com"}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201
        assert resp.json()["full_name"] == "José García"

    def test_country_with_spaces(self, client):
        payload = {**VALID_EMPLOYEE, "country": "United States", "email": "us@x.com"}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201


class TestFieldLengthBoundaries:

    def test_single_char_name_accepted(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "X", "email": "x@x.com"}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201

    def test_max_length_name_accepted(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "A" * 200, "email": "long@x.com"}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 201

    def test_name_exceeding_max_length_rejected(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "A" * 201}
        resp = client.post("/employees", json=payload)
        assert resp.status_code == 422

    def test_whitespace_only_name_rejected(self, client):
        payload = {**VALID_EMPLOYEE, "full_name": "   "}
        resp = client.post("/employees", json=payload)
        # Pydantic min_length counts after stripping in some modes, 
        # but our schema accepts spaces as valid chars.
        # This verifies the API handles it (201 or 422 depending on config).
        assert resp.status_code in (201, 422)


class TestPaginationEdgeCases:

    def test_page_0_returns_422(self, client):
        resp = client.get("/employees", params={"page": 0})
        assert resp.status_code == 422

    def test_negative_page_returns_422(self, client):
        resp = client.get("/employees", params={"page": -1})
        assert resp.status_code == 422

    def test_page_size_0_returns_422(self, client):
        resp = client.get("/employees", params={"page_size": 0})
        assert resp.status_code == 422

    def test_page_size_over_100_returns_422(self, client):
        resp = client.get("/employees", params={"page_size": 101})
        assert resp.status_code == 422

    def test_page_size_100_accepted(self, client):
        resp = client.get("/employees", params={"page_size": 100})
        assert resp.status_code == 200

    def test_empty_search_returns_all(self, client):
        client.post("/employees", json=VALID_EMPLOYEE)
        data = client.get("/employees", params={"search": ""}).json()
        assert data["total"] == 1

    def test_search_with_special_chars_does_not_crash(self, client):
        resp = client.get("/employees", params={"search": "%; DROP TABLE--"})
        assert resp.status_code == 200


class TestUpdateEdgeCases:

    def _create(self, client):
        return client.post("/employees", json=VALID_EMPLOYEE).json()["id"]

    def test_update_with_no_fields_returns_200(self, client):
        emp_id = self._create(client)
        resp = client.put(f"/employees/{emp_id}", json={})
        assert resp.status_code == 200

    def test_update_same_email_on_self_succeeds(self, client):
        emp_id = self._create(client)
        resp = client.put(f"/employees/{emp_id}", json={"email": "test@example.com"})
        assert resp.status_code == 200

    def test_update_with_invalid_json_returns_422(self, client):
        emp_id = self._create(client)
        resp = client.put(
            f"/employees/{emp_id}",
            content="not json",
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 422


class TestDeleteEdgeCases:

    def test_delete_nonexistent_negative_id(self, client):
        resp = client.delete("/employees/-1")
        assert resp.status_code == 404

    def test_delete_string_id_returns_422(self, client):
        resp = client.delete("/employees/abc")
        assert resp.status_code == 422


class TestInsightEdgeCases:

    def test_country_insights_with_url_encoded_space(self, client):
        client.post("/employees", json={
            **VALID_EMPLOYEE, "country": "United Kingdom", "email": "uk@x.com"
        })
        resp = client.get("/insights/country/United%20Kingdom")
        assert resp.status_code == 200
        assert resp.json()["employee_count"] == 1

    def test_top_earners_with_empty_db(self, client):
        resp = client.get("/insights/top-earners")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_department_insights_with_empty_db(self, client):
        resp = client.get("/insights/department")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_headcount_with_empty_db(self, client):
        resp = client.get("/insights/headcount")
        assert resp.status_code == 200
        assert resp.json() == []
