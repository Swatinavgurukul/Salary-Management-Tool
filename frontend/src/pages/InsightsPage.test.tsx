import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import InsightsPage from "./InsightsPage";

vi.mock("../api/client", () => ({
  fetchCountryInsight: vi.fn(),
  fetchJobInsight: vi.fn(),
  fetchDepartmentInsights: vi.fn().mockResolvedValue([]),
  fetchHeadcount: vi.fn().mockResolvedValue([]),
  fetchTopEarners: vi.fn().mockResolvedValue([]),
}));

describe("InsightsPage", () => {
  it("renders the page title", () => {
    render(<InsightsPage />);
    expect(screen.getByText("Salary Insights")).toBeInTheDocument();
  });

  it("renders country insights section", () => {
    render(<InsightsPage />);
    expect(screen.getByText("Country Insights")).toBeInTheDocument();
  });

  it("renders job title insights section", () => {
    render(<InsightsPage />);
    expect(screen.getByText("Job Title Insights")).toBeInTheDocument();
  });

  it("renders department breakdown section", () => {
    render(<InsightsPage />);
    expect(screen.getByText("Department Breakdown")).toBeInTheDocument();
  });

  it("renders headcount by country section", () => {
    render(<InsightsPage />);
    expect(screen.getByText("Headcount by Country")).toBeInTheDocument();
  });

  it("renders top earners section", () => {
    render(<InsightsPage />);
    expect(screen.getByText("Top 10 Earners")).toBeInTheDocument();
  });

  it("has search buttons", () => {
    render(<InsightsPage />);
    const buttons = screen.getAllByText("Search");
    expect(buttons.length).toBe(2);
  });
});
