"""TDD — Pagination for GET /employees.

RED phase: current endpoint returns all rows with no pagination support.
"""
import pytest


def _seed(client, count=25):
    for i in range(count):
        client.post("/employees", json={
            "full_name": f"Employee {i}",
            "job_title": "Dev",
            "country": "US",
            "salary": 50000 + i,
            "department": "Eng",
            "email": f"emp{i}@x.com",
        })


class TestPagination:

    def test_default_page_returns_paginated_response_shape(self, client):
        _seed(client, 5)
        resp = client.get("/employees")
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data

    def test_default_page_size_is_20(self, client):
        _seed(client, 25)
        data = client.get("/employees").json()
        assert len(data["items"]) == 20
        assert data["page_size"] == 20

    def test_total_reflects_all_employees(self, client):
        _seed(client, 25)
        data = client.get("/employees").json()
        assert data["total"] == 25

    def test_page_2_returns_remaining(self, client):
        _seed(client, 25)
        data = client.get("/employees", params={"page": 2}).json()
        assert len(data["items"]) == 5
        assert data["page"] == 2

    def test_custom_page_size(self, client):
        _seed(client, 15)
        data = client.get("/employees", params={"page_size": 5}).json()
        assert len(data["items"]) == 5
        assert data["total"] == 15

    def test_empty_page_returns_empty_items(self, client):
        _seed(client, 5)
        data = client.get("/employees", params={"page": 100}).json()
        assert data["items"] == []
        assert data["total"] == 5

    def test_search_filters_by_name(self, client):
        _seed(client, 10)
        client.post("/employees", json={
            "full_name": "Unique Person",
            "job_title": "Manager",
            "country": "India",
            "salary": 99000,
            "department": "Ops",
            "email": "unique@x.com",
        })
        data = client.get("/employees", params={"search": "Unique"}).json()
        assert data["total"] == 1
        assert data["items"][0]["full_name"] == "Unique Person"

    def test_search_filters_by_country(self, client):
        _seed(client, 3)
        client.post("/employees", json={
            "full_name": "Indian Person",
            "job_title": "Dev",
            "country": "India",
            "salary": 60000,
            "department": "Eng",
            "email": "india@x.com",
        })
        data = client.get("/employees", params={"search": "India"}).json()
        assert data["total"] == 1
