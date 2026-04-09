"""Seed the database with 10,000 employees.

Reads first_names.txt and last_names.txt, generates all unique
(first, last) combinations, and bulk-inserts them into SQLite.
Designed to be run repeatedly — clears existing data each time.

Usage:
    python seed.py            # seeds 10,000 employees
    python seed.py --count 500  # seeds 500 employees (for quick testing)
"""
import argparse
import random
import time
from pathlib import Path

from sqlalchemy import text

from app.database import engine, Base, SessionLocal
from app.models import Employee  # noqa: F401 — registers the table

DATA_DIR = Path(__file__).parent / "data"

JOB_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer",
    "Data Analyst", "Senior Data Analyst", "Data Scientist",
    "Product Manager", "Senior Product Manager", "Director of Product",
    "UX Designer", "Senior UX Designer", "UI Designer",
    "DevOps Engineer", "Site Reliability Engineer", "Cloud Architect",
    "QA Engineer", "Senior QA Engineer", "Test Lead",
    "Engineering Manager", "VP of Engineering",
    "HR Manager", "HR Business Partner", "Recruiter",
    "Finance Analyst", "Senior Finance Analyst", "Controller",
    "Marketing Manager", "Content Strategist", "Growth Analyst",
    "Sales Representative", "Account Executive", "Sales Manager",
]

DEPARTMENTS = {
    "Software Engineer": "Engineering", "Senior Software Engineer": "Engineering",
    "Staff Engineer": "Engineering", "Engineering Manager": "Engineering",
    "VP of Engineering": "Engineering",
    "Data Analyst": "Data", "Senior Data Analyst": "Data",
    "Data Scientist": "Data",
    "Product Manager": "Product", "Senior Product Manager": "Product",
    "Director of Product": "Product",
    "UX Designer": "Design", "Senior UX Designer": "Design",
    "UI Designer": "Design",
    "DevOps Engineer": "Infrastructure", "Site Reliability Engineer": "Infrastructure",
    "Cloud Architect": "Infrastructure",
    "QA Engineer": "Quality Assurance", "Senior QA Engineer": "Quality Assurance",
    "Test Lead": "Quality Assurance",
    "HR Manager": "Human Resources", "HR Business Partner": "Human Resources",
    "Recruiter": "Human Resources",
    "Finance Analyst": "Finance", "Senior Finance Analyst": "Finance",
    "Controller": "Finance",
    "Marketing Manager": "Marketing", "Content Strategist": "Marketing",
    "Growth Analyst": "Marketing",
    "Sales Representative": "Sales", "Account Executive": "Sales",
    "Sales Manager": "Sales",
}

COUNTRIES = [
    "India", "United States", "United Kingdom", "Germany", "Canada",
    "Australia", "France", "Japan", "Brazil", "Singapore",
]

SALARY_RANGES = {
    "India":         (400_000, 4_000_000),
    "United States": (50_000, 250_000),
    "United Kingdom": (35_000, 180_000),
    "Germany":       (40_000, 170_000),
    "Canada":        (45_000, 200_000),
    "Australia":     (50_000, 200_000),
    "France":        (35_000, 160_000),
    "Japan":         (3_500_000, 15_000_000),
    "Brazil":        (30_000, 150_000),
    "Singapore":     (40_000, 200_000),
}


def load_names(filename: str) -> list:
    filepath = DATA_DIR / filename
    with open(filepath) as f:
        return [line.strip() for line in f if line.strip()]


def generate_employees(count: int) -> list:
    first_names = load_names("first_names.txt")
    last_names = load_names("last_names.txt")

    if len(first_names) * len(last_names) < count:
        raise ValueError(
            f"Need at least {count} unique name combos, "
            f"but only have {len(first_names)} x {len(last_names)} = "
            f"{len(first_names) * len(last_names)}"
        )

    all_combos = [(f, l) for f in first_names for l in last_names]
    random.shuffle(all_combos)
    selected = all_combos[:count]

    employees = []
    for first, last in selected:
        job_title = random.choice(JOB_TITLES)
        country = random.choice(COUNTRIES)
        lo, hi = SALARY_RANGES[country]
        salary = round(random.uniform(lo, hi), 2)

        employees.append({
            "full_name": f"{first} {last}",
            "job_title": job_title,
            "department": DEPARTMENTS[job_title],
            "country": country,
            "salary": salary,
            "email": f"{first.lower()}.{last.lower()}@company.com",
        })

    return employees


def seed(count: int = 10_000):
    print(f"Seeding {count:,} employees...")
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        deleted = session.query(Employee).delete()
        session.commit()
        if deleted:
            print(f"  Cleared {deleted:,} existing rows.")

        t0 = time.perf_counter()
        employees = generate_employees(count)
        t_gen = time.perf_counter() - t0
        print(f"  Generated {len(employees):,} records in {t_gen:.2f}s")

        t0 = time.perf_counter()
        BATCH_SIZE = 1000
        for i in range(0, len(employees), BATCH_SIZE):
            batch = employees[i:i + BATCH_SIZE]
            session.execute(Employee.__table__.insert(), batch)
            session.commit()
        t_insert = time.perf_counter() - t0
        print(f"  Inserted in {t_insert:.2f}s ({BATCH_SIZE}-row batches)")

        total = session.query(Employee).count()
        print(f"  Total employees in DB: {total:,}")
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the employee database")
    parser.add_argument("--count", type=int, default=10_000,
                        help="Number of employees to generate (default: 10000)")
    args = parser.parse_args()
    seed(args.count)
