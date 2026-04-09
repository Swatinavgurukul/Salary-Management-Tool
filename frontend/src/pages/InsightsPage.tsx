import { useState, useEffect } from "react";
import type {
  CountryInsight,
  JobInsight,
  DepartmentInsight,
  HeadcountEntry,
  Employee,
} from "../types/employee";
import {
  fetchCountryInsight,
  fetchJobInsight,
  fetchDepartmentInsights,
  fetchHeadcount,
  fetchTopEarners,
} from "../api/client";

function fmt(n: number) {
  return n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function InsightsPage() {
  const [country, setCountry] = useState("");
  const [countryData, setCountryData] = useState<CountryInsight | null>(null);
  const [countryError, setCountryError] = useState("");

  const [jobTitle, setJobTitle] = useState("");
  const [jobCountry, setJobCountry] = useState("");
  const [jobData, setJobData] = useState<JobInsight | null>(null);
  const [jobError, setJobError] = useState("");

  const [departments, setDepartments] = useState<DepartmentInsight[]>([]);
  const [headcount, setHeadcount] = useState<HeadcountEntry[]>([]);
  const [topEarners, setTopEarners] = useState<Employee[]>([]);

  useEffect(() => {
    fetchDepartmentInsights().then(setDepartments).catch(() => {});
    fetchHeadcount().then(setHeadcount).catch(() => {});
    fetchTopEarners(10).then(setTopEarners).catch(() => {});
  }, []);

  const handleCountrySearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setCountryError("");
    setCountryData(null);
    try {
      setCountryData(await fetchCountryInsight(country));
    } catch {
      setCountryError("No data found for this country");
    }
  };

  const handleJobSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setJobError("");
    setJobData(null);
    try {
      setJobData(await fetchJobInsight(jobTitle, jobCountry || undefined));
    } catch {
      setJobError("No data found for this filter");
    }
  };

  return (
    <div>
      <h2>Salary Insights</h2>

      {/* Row 1: Search-based insights */}
      <div className="insights-grid">
        <section className="insight-card">
          <h3>Country Insights</h3>
          <p className="subtitle">Min, max, and average salary by country</p>
          <form onSubmit={handleCountrySearch} className="insight-form">
            <input
              placeholder="Enter country (e.g. India)"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              required
            />
            <button type="submit" className="btn btn-primary">Search</button>
          </form>
          {countryError && <p className="error">{countryError}</p>}
          {countryData && (
            <div className="insight-results">
              <h4>{countryData.country}</h4>
              <table className="stats-table">
                <tbody>
                  <tr><td>Employees</td><td><strong>{countryData.employee_count}</strong></td></tr>
                  <tr><td>Min Salary</td><td>{fmt(countryData.min_salary)}</td></tr>
                  <tr><td>Max Salary</td><td>{fmt(countryData.max_salary)}</td></tr>
                  <tr><td>Avg Salary</td><td><strong>{fmt(countryData.avg_salary)}</strong></td></tr>
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="insight-card">
          <h3>Job Title Insights</h3>
          <p className="subtitle">Average salary by job title, optionally filtered by country</p>
          <form onSubmit={handleJobSearch} className="insight-form">
            <input
              placeholder="Job title (e.g. Software Engineer)"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              required
            />
            <input
              placeholder="Country (optional)"
              value={jobCountry}
              onChange={(e) => setJobCountry(e.target.value)}
            />
            <button type="submit" className="btn btn-primary">Search</button>
          </form>
          {jobError && <p className="error">{jobError}</p>}
          {jobData && (
            <div className="insight-results">
              <h4>{jobData.job_title}{jobData.country ? ` in ${jobData.country}` : " (all countries)"}</h4>
              <table className="stats-table">
                <tbody>
                  <tr><td>Employees</td><td><strong>{jobData.employee_count}</strong></td></tr>
                  <tr><td>Min Salary</td><td>{fmt(jobData.min_salary)}</td></tr>
                  <tr><td>Max Salary</td><td>{fmt(jobData.max_salary)}</td></tr>
                  <tr><td>Avg Salary</td><td><strong>{fmt(jobData.avg_salary)}</strong></td></tr>
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>

      {/* Row 2: Auto-loaded dashboards */}
      <div className="insights-grid" style={{ marginTop: "2rem" }}>
        <section className="insight-card">
          <h3>Headcount by Country</h3>
          <p className="subtitle">Employee distribution across countries</p>
          {headcount.length > 0 && (
            <table className="data-table compact">
              <thead>
                <tr><th>Country</th><th>Employees</th><th>Avg Salary</th></tr>
              </thead>
              <tbody>
                {headcount.map((h) => (
                  <tr key={h.country}>
                    <td>{h.country}</td>
                    <td>{h.employee_count}</td>
                    <td>{fmt(h.avg_salary)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <section className="insight-card">
          <h3>Department Breakdown</h3>
          <p className="subtitle">Salary stats per department</p>
          {departments.length > 0 && (
            <table className="data-table compact">
              <thead>
                <tr><th>Department</th><th>Count</th><th>Avg</th><th>Min</th><th>Max</th></tr>
              </thead>
              <tbody>
                {departments.map((d) => (
                  <tr key={d.department}>
                    <td>{d.department}</td>
                    <td>{d.employee_count}</td>
                    <td>{fmt(d.avg_salary)}</td>
                    <td>{fmt(d.min_salary)}</td>
                    <td>{fmt(d.max_salary)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </div>

      {/* Row 3: Top earners */}
      <div style={{ marginTop: "2rem" }}>
        <section className="insight-card">
          <h3>Top 10 Earners</h3>
          <p className="subtitle">Highest paid employees in the organization</p>
          {topEarners.length > 0 && (
            <table className="data-table compact">
              <thead>
                <tr><th>#</th><th>Name</th><th>Job Title</th><th>Country</th><th>Salary</th></tr>
              </thead>
              <tbody>
                {topEarners.map((e, i) => (
                  <tr key={e.id}>
                    <td>{i + 1}</td>
                    <td>{e.full_name}</td>
                    <td>{e.job_title}</td>
                    <td>{e.country}</td>
                    <td>{e.salary.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </div>
    </div>
  );
}
