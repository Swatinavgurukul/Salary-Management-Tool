import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import EmployeeListPage from "./EmployeeListPage";
import * as client from "../api/client";
import type { Employee } from "../types/employee";

vi.mock("../api/client");

const mockEmployees: Employee[] = [
  {
    id: 1,
    full_name: "Alice Smith",
    job_title: "Engineer",
    country: "India",
    salary: 80000,
    department: "Engineering",
    email: "alice@example.com",
    created_at: "2024-01-01T00:00:00",
    updated_at: null,
  },
  {
    id: 2,
    full_name: "Bob Jones",
    job_title: "Designer",
    country: "US",
    salary: 90000,
    department: "Design",
    email: "bob@example.com",
    created_at: "2024-01-01T00:00:00",
    updated_at: null,
  },
];

function renderPage() {
  return render(
    <MemoryRouter>
      <EmployeeListPage />
    </MemoryRouter>
  );
}

describe("EmployeeListPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows loading state initially", () => {
    vi.mocked(client.fetchEmployees).mockReturnValue(new Promise(() => {}));
    renderPage();
    expect(screen.getByText("Loading employees...")).toBeInTheDocument();
  });

  it("renders employee table after loading", async () => {
    vi.mocked(client.fetchEmployees).mockResolvedValue(mockEmployees);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Alice Smith")).toBeInTheDocument();
    });
    expect(screen.getByText("Bob Jones")).toBeInTheDocument();
  });

  it("shows empty state when no employees", async () => {
    vi.mocked(client.fetchEmployees).mockResolvedValue([]);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("No employees found.")).toBeInTheDocument();
    });
  });

  it("displays employee count in header", async () => {
    vi.mocked(client.fetchEmployees).mockResolvedValue(mockEmployees);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Employees (2)")).toBeInTheDocument();
    });
  });

  it("has an Add Employee button", async () => {
    vi.mocked(client.fetchEmployees).mockResolvedValue([]);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("+ Add Employee")).toBeInTheDocument();
    });
  });

  it("shows error message on fetch failure", async () => {
    vi.mocked(client.fetchEmployees).mockRejectedValue(new Error("fail"));
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Failed to load employees")).toBeInTheDocument();
    });
  });
});
