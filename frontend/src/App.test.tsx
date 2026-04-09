import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import App from "./App";

vi.mock("./api/client", () => ({
  fetchEmployees: vi.fn().mockResolvedValue([]),
  fetchEmployee: vi.fn(),
  createEmployee: vi.fn(),
  updateEmployee: vi.fn(),
  deleteEmployee: vi.fn(),
  fetchCountryInsight: vi.fn(),
  fetchJobInsight: vi.fn(),
}));

describe("App", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the application title", () => {
    render(<App />);
    expect(screen.getByText("Salary Management")).toBeInTheDocument();
  });

  it("renders the navigation links", () => {
    render(<App />);
    expect(screen.getByText("Employees")).toBeInTheDocument();
    expect(screen.getByText("Insights")).toBeInTheDocument();
  });

  it("shows the employee list page by default", async () => {
    render(<App />);
    expect(
      await screen.findByText("No employees found.")
    ).toBeInTheDocument();
  });
});
