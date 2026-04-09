"""TDD Step 6 — Salary Insights API tests.

RED phase: /insights endpoints do not exist yet, so all tests will fail.
"""
import pytest


def _seed_employees(client):
    """Seed a realistic mix of employees across countries and job titles."""
    employees = [
        {"full_name": "A1", "job_title": "Engineer", "country": "India",
         "salary": 60000, "department": "Eng", "email": "a1@x.com"},
        {"full_name": "A2", "job_title": "Engineer", "country": "India",
         "salary": 80000, "department": "Eng", "email": "a2@x.com"},
        {"full_name": "A3", "job_title": "Designer", "country": "India",
         "salary": 50000, "department": "Design", "email": "a3@x.com"},
        {"full_name": "B1", "job_title": "Engineer", "country": "US",
         "salary": 120000, "department": "Eng", "email": "b1@x.com"},
        {"full_name": "B2", "job_title": "Engineer", "country": "US",
         "salary": 140000, "department": "Eng", "email": "b2@x.com"},
        {"full_name": "B3", "job_title": "Manager", "country": "US",
         "salary": 150000, "department": "Ops", "email": "b3@x.com"},
    ]
    for emp in employees:
        client.post("/employees", json=emp)


# ── GET /insights/country/{country} ───────────────────────────

class TestCountryInsights:

    def test_returns_200(self, client):
        _seed_employees(client)
        response = client.get("/insights/country/India")
        assert response.status_code == 200

    def test_returns_min_max_avg_for_country(self, client):
        _seed_employees(client)
        data = client.get("/insights/country/India").json()
        assert "min_salary" in data
        assert "max_salary" in data
        assert "avg_salary" in data

    def test_correct_aggregates_for_india(self, client):
        """India has salaries 60k, 80k, 50k → min=50k, max=80k, avg=~63333."""
        _seed_employees(client)
        data = client.get("/insights/country/India").json()
        assert data["min_salary"] == 50000
        assert data["max_salary"] == 80000
        assert round(data["avg_salary"], 2) == round(190000 / 3, 2)

    def test_correct_aggregates_for_us(self, client):
        """US has salaries 120k, 140k, 150k → min=120k, max=150k, avg=~136667."""
        _seed_employees(client)
        data = client.get("/insights/country/US").json()
        assert data["min_salary"] == 120000
        assert data["max_salary"] == 150000
        assert round(data["avg_salary"], 2) == round(410000 / 3, 2)

    def test_includes_employee_count(self, client):
        _seed_employees(client)
        data = client.get("/insights/country/India").json()
        assert data["employee_count"] == 3

    def test_returns_404_for_unknown_country(self, client):
        _seed_employees(client)
        response = client.get("/insights/country/Antarctica")
        assert response.status_code == 404

    def test_country_lookup_is_case_insensitive(self, client):
        _seed_employees(client)
        data = client.get("/insights/country/india").json()
        assert data["employee_count"] == 3


# ── GET /insights/job ─────────────────────────────────────────

class TestJobInsights:

    def test_returns_200_with_valid_filters(self, client):
        _seed_employees(client)
        response = client.get("/insights/job", params={
            "job_title": "Engineer", "country": "India"
        })
        assert response.status_code == 200

    def test_returns_avg_salary_for_job_in_country(self, client):
        """Engineers in India: 60k, 80k → avg = 70k."""
        _seed_employees(client)
        data = client.get("/insights/job", params={
            "job_title": "Engineer", "country": "India"
        }).json()
        assert data["avg_salary"] == 70000

    def test_returns_min_max_for_job_in_country(self, client):
        _seed_employees(client)
        data = client.get("/insights/job", params={
            "job_title": "Engineer", "country": "US"
        }).json()
        assert data["min_salary"] == 120000
        assert data["max_salary"] == 140000

    def test_includes_employee_count(self, client):
        _seed_employees(client)
        data = client.get("/insights/job", params={
            "job_title": "Engineer", "country": "US"
        }).json()
        assert data["employee_count"] == 2

    def test_returns_404_when_no_matching_employees(self, client):
        _seed_employees(client)
        response = client.get("/insights/job", params={
            "job_title": "CEO", "country": "India"
        })
        assert response.status_code == 404

    def test_job_title_filter_is_case_insensitive(self, client):
        _seed_employees(client)
        data = client.get("/insights/job", params={
            "job_title": "engineer", "country": "India"
        }).json()
        assert data["employee_count"] == 2

    def test_job_filter_without_country_returns_all_countries(self, client):
        """Engineer across all countries: 60k, 80k, 120k, 140k → 4 people."""
        _seed_employees(client)
        data = client.get("/insights/job", params={
            "job_title": "Engineer"
        }).json()
        assert data["employee_count"] == 4
        assert data["avg_salary"] == 100000

    def test_requires_at_least_job_title(self, client):
        response = client.get("/insights/job")
        assert response.status_code == 422
