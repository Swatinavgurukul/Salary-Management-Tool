"""TDD tests for seeding logic — validates data generation before DB insert."""
import pytest
from seed import load_names, generate_employees, JOB_TITLES, COUNTRIES, DEPARTMENTS


class TestLoadNames:

    def test_loads_first_names(self):
        names = load_names("first_names.txt")
        assert len(names) == 100

    def test_loads_last_names(self):
        names = load_names("last_names.txt")
        assert len(names) == 100

    def test_no_blank_lines(self):
        for filename in ("first_names.txt", "last_names.txt"):
            names = load_names(filename)
            assert all(name.strip() != "" for name in names)


class TestGenerateEmployees:

    def test_generates_requested_count(self):
        employees = generate_employees(100)
        assert len(employees) == 100

    def test_generates_10000_employees(self):
        employees = generate_employees(10_000)
        assert len(employees) == 10_000

    def test_all_emails_unique(self):
        employees = generate_employees(10_000)
        emails = [e["email"] for e in employees]
        assert len(emails) == len(set(emails))

    def test_full_name_from_name_files(self):
        first_names = set(load_names("first_names.txt"))
        last_names = set(load_names("last_names.txt"))
        employees = generate_employees(50)
        for emp in employees:
            first, last = emp["full_name"].split(" ", 1)
            assert first in first_names
            assert last in last_names

    def test_employee_has_all_required_fields(self):
        employees = generate_employees(10)
        required = {"full_name", "job_title", "department", "country", "salary", "email"}
        for emp in employees:
            assert required.issubset(emp.keys())

    def test_salary_is_positive(self):
        employees = generate_employees(500)
        for emp in employees:
            assert emp["salary"] > 0

    def test_job_title_from_valid_list(self):
        employees = generate_employees(200)
        for emp in employees:
            assert emp["job_title"] in JOB_TITLES

    def test_country_from_valid_list(self):
        employees = generate_employees(200)
        for emp in employees:
            assert emp["country"] in COUNTRIES

    def test_department_matches_job_title(self):
        employees = generate_employees(200)
        for emp in employees:
            assert emp["department"] == DEPARTMENTS[emp["job_title"]]

    def test_raises_if_count_exceeds_unique_combos(self):
        with pytest.raises(ValueError, match="unique name combos"):
            generate_employees(10_001)
