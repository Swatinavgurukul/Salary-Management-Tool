"""TDD — Additional meaningful metrics for HR Manager (Req 2c).

RED phase: these endpoints do not exist yet.
"""


def _seed(client):
    employees = [
        {"full_name": "A1", "job_title": "Engineer", "country": "India",
         "salary": 60000, "department": "Engineering", "email": "a1@x.com"},
        {"full_name": "A2", "job_title": "Engineer", "country": "India",
         "salary": 80000, "department": "Engineering", "email": "a2@x.com"},
        {"full_name": "A3", "job_title": "Designer", "country": "India",
         "salary": 50000, "department": "Design", "email": "a3@x.com"},
        {"full_name": "B1", "job_title": "Engineer", "country": "US",
         "salary": 120000, "department": "Engineering", "email": "b1@x.com"},
        {"full_name": "B2", "job_title": "Manager", "country": "US",
         "salary": 150000, "department": "Operations", "email": "b2@x.com"},
        {"full_name": "B3", "job_title": "Manager", "country": "US",
         "salary": 140000, "department": "Operations", "email": "b3@x.com"},
    ]
    for emp in employees:
        client.post("/employees", json=emp)


class TestDepartmentInsights:
    """GET /insights/department — breakdown by department."""

    def test_returns_200(self, client):
        _seed(client)
        resp = client.get("/insights/department")
        assert resp.status_code == 200

    def test_returns_list_of_departments(self, client):
        _seed(client)
        data = client.get("/insights/department").json()
        assert isinstance(data, list)
        assert len(data) >= 3

    def test_each_entry_has_aggregates(self, client):
        _seed(client)
        data = client.get("/insights/department").json()
        for entry in data:
            assert "department" in entry
            assert "employee_count" in entry
            assert "avg_salary" in entry
            assert "min_salary" in entry
            assert "max_salary" in entry


class TestHeadcountByCountry:
    """GET /insights/headcount — employee count per country."""

    def test_returns_200(self, client):
        _seed(client)
        resp = client.get("/insights/headcount")
        assert resp.status_code == 200

    def test_returns_list_sorted_by_count_desc(self, client):
        _seed(client)
        data = client.get("/insights/headcount").json()
        assert isinstance(data, list)
        counts = [d["employee_count"] for d in data]
        assert counts == sorted(counts, reverse=True)

    def test_each_entry_has_country_and_count(self, client):
        _seed(client)
        data = client.get("/insights/headcount").json()
        for entry in data:
            assert "country" in entry
            assert "employee_count" in entry
            assert "avg_salary" in entry


class TestTopEarners:
    """GET /insights/top-earners — highest paid employees."""

    def test_returns_200(self, client):
        _seed(client)
        resp = client.get("/insights/top-earners")
        assert resp.status_code == 200

    def test_default_limit_is_10(self, client):
        _seed(client)
        data = client.get("/insights/top-earners").json()
        assert isinstance(data, list)
        assert len(data) <= 10

    def test_sorted_by_salary_desc(self, client):
        _seed(client)
        data = client.get("/insights/top-earners").json()
        salaries = [d["salary"] for d in data]
        assert salaries == sorted(salaries, reverse=True)

    def test_custom_limit(self, client):
        _seed(client)
        data = client.get("/insights/top-earners", params={"limit": 3}).json()
        assert len(data) == 3

    def test_highest_salary_is_first(self, client):
        _seed(client)
        data = client.get("/insights/top-earners", params={"limit": 1}).json()
        assert data[0]["salary"] == 150000
