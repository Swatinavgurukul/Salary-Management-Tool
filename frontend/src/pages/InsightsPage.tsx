import { useState } from "react";
import type { CountryInsight, JobInsight } from "../types/employee";
import { fetchCountryInsight, fetchJobInsight } from "../api/client";

function formatSalary(n: number) {
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

  const handleCountrySearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setCountryError("");
    setCountryData(null);
    try {
      const data = await fetchCountryInsight(country);
      setCountryData(data);
    } catch {
      setCountryError("No data found for this country");
    }
  };

  const handleJobSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setJobError("");
    setJobData(null);
    try {
      const data = await fetchJobInsight(jobTitle, jobCountry || undefined);
      setJobData(data);
    } catch {
      setJobError("No data found for this filter");
    }
  };

  return (
    <div>
      <h2>Salary Insights</h2>

      <div className="insights-grid">
        {/* Country Insights */}
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
            <button type="submit" className="btn btn-primary">
              Search
            </button>
          </form>

          {countryError && <p className="error">{countryError}</p>}

          {countryData && (
            <div className="insight-results">
              <h4>{countryData.country}</h4>
              <table className="stats-table">
                <tbody>
                  <tr>
                    <td>Employees</td>
                    <td><strong>{countryData.employee_count}</strong></td>
                  </tr>
                  <tr>
                    <td>Min Salary</td>
                    <td>{formatSalary(countryData.min_salary)}</td>
                  </tr>
                  <tr>
                    <td>Max Salary</td>
                    <td>{formatSalary(countryData.max_salary)}</td>
                  </tr>
                  <tr>
                    <td>Avg Salary</td>
                    <td><strong>{formatSalary(countryData.avg_salary)}</strong></td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Job Title Insights */}
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
            <button type="submit" className="btn btn-primary">
              Search
            </button>
          </form>

          {jobError && <p className="error">{jobError}</p>}

          {jobData && (
            <div className="insight-results">
              <h4>
                {jobData.job_title}
                {jobData.country ? ` in ${jobData.country}` : " (all countries)"}
              </h4>
              <table className="stats-table">
                <tbody>
                  <tr>
                    <td>Employees</td>
                    <td><strong>{jobData.employee_count}</strong></td>
                  </tr>
                  <tr>
                    <td>Min Salary</td>
                    <td>{formatSalary(jobData.min_salary)}</td>
                  </tr>
                  <tr>
                    <td>Max Salary</td>
                    <td>{formatSalary(jobData.max_salary)}</td>
                  </tr>
                  <tr>
                    <td>Avg Salary</td>
                    <td><strong>{formatSalary(jobData.avg_salary)}</strong></td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
