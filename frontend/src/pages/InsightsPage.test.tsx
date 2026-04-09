import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import InsightsPage from "./InsightsPage";

vi.mock("../api/client");

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

  it("has search buttons", () => {
    render(<InsightsPage />);
    const buttons = screen.getAllByText("Search");
    expect(buttons.length).toBe(2);
  });
});
