import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import EmployeeFormPage from "./EmployeeFormPage";
import * as client from "../api/client";
import type { Employee } from "../types/employee";

vi.mock("../api/client");

const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return { ...actual, useNavigate: () => mockNavigate };
});

const sampleEmployee: Employee = {
  id: 42,
  full_name: "Alice Smith",
  job_title: "Engineer",
  country: "India",
  salary: 80000,
  department: "Engineering",
  email: "alice@example.com",
  created_at: "2024-01-01T00:00:00",
  updated_at: null,
};

function renderNew() {
  return render(
    <MemoryRouter initialEntries={["/employees/new"]}>
      <Routes>
        <Route path="/employees/new" element={<EmployeeFormPage />} />
      </Routes>
    </MemoryRouter>
  );
}

function renderEdit(id = 42) {
  return render(
    <MemoryRouter initialEntries={[`/employees/${id}/edit`]}>
      <Routes>
        <Route path="/employees/:id/edit" element={<EmployeeFormPage />} />
      </Routes>
    </MemoryRouter>
  );
}

describe("EmployeeFormPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Create mode", () => {
    it("renders the Add Employee heading", () => {
      renderNew();
      expect(screen.getByText("Add Employee")).toBeInTheDocument();
    });

    it("renders all form fields", () => {
      renderNew();
      expect(screen.getByLabelText(/full name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/job title/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/department/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/country/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/salary/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    });

    it("renders Create and Cancel buttons", () => {
      renderNew();
      expect(screen.getByRole("button", { name: "Create" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Cancel" })).toBeInTheDocument();
    });

    it("calls createEmployee on submit and navigates home", async () => {
      vi.mocked(client.createEmployee).mockResolvedValue(sampleEmployee);
      const user = userEvent.setup();
      renderNew();

      await user.type(screen.getByLabelText(/full name/i), "Alice Smith");
      await user.type(screen.getByLabelText(/job title/i), "Engineer");
      await user.type(screen.getByLabelText(/department/i), "Engineering");
      await user.type(screen.getByLabelText(/country/i), "India");
      await user.type(screen.getByLabelText(/salary/i), "80000");
      await user.type(screen.getByLabelText(/email/i), "alice@example.com");

      await user.click(screen.getByRole("button", { name: "Create" }));

      await waitFor(() => {
        expect(client.createEmployee).toHaveBeenCalledTimes(1);
      });
      expect(mockNavigate).toHaveBeenCalledWith("/");
    });

    it("shows API error string on failure", async () => {
      vi.mocked(client.createEmployee).mockRejectedValue({
        response: { data: { detail: "An employee with this email already exists." } },
      });
      const user = userEvent.setup();
      renderNew();

      await user.type(screen.getByLabelText(/full name/i), "Alice Smith");
      await user.type(screen.getByLabelText(/job title/i), "Engineer");
      await user.type(screen.getByLabelText(/department/i), "Engineering");
      await user.type(screen.getByLabelText(/country/i), "India");
      await user.type(screen.getByLabelText(/salary/i), "80000");
      await user.type(screen.getByLabelText(/email/i), "alice@example.com");

      await user.click(screen.getByRole("button", { name: "Create" }));

      await waitFor(() => {
        expect(
          screen.getByText("An employee with this email already exists.")
        ).toBeInTheDocument();
      });
    });

    it("shows validation error array from API", async () => {
      vi.mocked(client.createEmployee).mockRejectedValue({
        response: {
          data: {
            detail: [
              { msg: "field required", loc: ["body", "full_name"] },
              { msg: "salary must be > 0", loc: ["body", "salary"] },
            ],
          },
        },
      });
      const user = userEvent.setup();
      renderNew();

      await user.type(screen.getByLabelText(/full name/i), "X");
      await user.type(screen.getByLabelText(/job title/i), "Y");
      await user.type(screen.getByLabelText(/department/i), "Z");
      await user.type(screen.getByLabelText(/country/i), "W");
      await user.type(screen.getByLabelText(/salary/i), "1");
      await user.type(screen.getByLabelText(/email/i), "x@y.com");

      await user.click(screen.getByRole("button", { name: "Create" }));

      await waitFor(() => {
        expect(
          screen.getByText("field required, salary must be > 0")
        ).toBeInTheDocument();
      });
    });

    it("shows fallback error when response has no detail", async () => {
      vi.mocked(client.createEmployee).mockRejectedValue(new Error("network"));
      const user = userEvent.setup();
      renderNew();

      await user.type(screen.getByLabelText(/full name/i), "X");
      await user.type(screen.getByLabelText(/job title/i), "Y");
      await user.type(screen.getByLabelText(/department/i), "Z");
      await user.type(screen.getByLabelText(/country/i), "W");
      await user.type(screen.getByLabelText(/salary/i), "1");
      await user.type(screen.getByLabelText(/email/i), "x@y.com");

      await user.click(screen.getByRole("button", { name: "Create" }));

      await waitFor(() => {
        expect(screen.getByText("Something went wrong")).toBeInTheDocument();
      });
    });

    it("navigates home when Cancel is clicked", async () => {
      const user = userEvent.setup();
      renderNew();
      await user.click(screen.getByRole("button", { name: "Cancel" }));
      expect(mockNavigate).toHaveBeenCalledWith("/");
    });
  });

  describe("Edit mode", () => {
    it("renders the Edit Employee heading", async () => {
      vi.mocked(client.fetchEmployee).mockResolvedValue(sampleEmployee);
      renderEdit();
      expect(screen.getByText("Edit Employee")).toBeInTheDocument();
    });

    it("populates form with existing employee data", async () => {
      vi.mocked(client.fetchEmployee).mockResolvedValue(sampleEmployee);
      renderEdit();

      await waitFor(() => {
        expect(screen.getByLabelText(/full name/i)).toHaveValue("Alice Smith");
      });
      expect(screen.getByLabelText(/job title/i)).toHaveValue("Engineer");
      expect(screen.getByLabelText(/department/i)).toHaveValue("Engineering");
      expect(screen.getByLabelText(/country/i)).toHaveValue("India");
      expect(screen.getByLabelText(/salary/i)).toHaveValue(80000);
      expect(screen.getByLabelText(/email/i)).toHaveValue("alice@example.com");
    });

    it("renders Update button instead of Create", async () => {
      vi.mocked(client.fetchEmployee).mockResolvedValue(sampleEmployee);
      renderEdit();
      await waitFor(() => {
        expect(screen.getByRole("button", { name: "Update" })).toBeInTheDocument();
      });
    });

    it("calls updateEmployee on submit", async () => {
      vi.mocked(client.fetchEmployee).mockResolvedValue(sampleEmployee);
      vi.mocked(client.updateEmployee).mockResolvedValue(sampleEmployee);
      const user = userEvent.setup();
      renderEdit();

      await waitFor(() => {
        expect(screen.getByLabelText(/full name/i)).toHaveValue("Alice Smith");
      });

      await user.click(screen.getByRole("button", { name: "Update" }));

      await waitFor(() => {
        expect(client.updateEmployee).toHaveBeenCalledTimes(1);
      });
      expect(mockNavigate).toHaveBeenCalledWith("/");
    });

    it("shows error when employee fetch fails", async () => {
      vi.mocked(client.fetchEmployee).mockRejectedValue(new Error("404"));
      renderEdit();

      await waitFor(() => {
        expect(screen.getByText("Employee not found")).toBeInTheDocument();
      });
    });
  });
});
