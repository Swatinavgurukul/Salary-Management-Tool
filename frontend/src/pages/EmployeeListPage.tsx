import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import type { Employee } from "../types/employee";
import { fetchEmployees, deleteEmployee } from "../api/client";

const PAGE_SIZE = 20;

export default function EmployeeListPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");

  const load = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchEmployees(page, PAGE_SIZE, search || undefined);
      setEmployees(data.items);
      setTotal(data.total);
    } catch {
      setError("Failed to load employees");
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    load();
  }, [load]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    setSearch(searchInput);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this employee?")) return;
    try {
      await deleteEmployee(id);
      load();
    } catch {
      setError("Failed to delete employee");
    }
  };

  const totalPages = Math.ceil(total / PAGE_SIZE);

  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <div className="page-header">
        <h2>Employees ({total})</h2>
        <Link to="/employees/new" className="btn btn-primary">
          + Add Employee
        </Link>
      </div>

      <form onSubmit={handleSearch} className="search-bar">
        <input
          type="text"
          placeholder="Search by name, title, country, department..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="btn btn-primary">Search</button>
        {search && (
          <button
            type="button"
            className="btn"
            onClick={() => { setSearchInput(""); setSearch(""); setPage(1); }}
          >
            Clear
          </button>
        )}
      </form>

      {loading ? (
        <p>Loading employees...</p>
      ) : (
        <>
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Job Title</th>
                <th>Department</th>
                <th>Country</th>
                <th>Salary</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.id}>
                  <td>{emp.full_name}</td>
                  <td>{emp.job_title}</td>
                  <td>{emp.department}</td>
                  <td>{emp.country}</td>
                  <td>{emp.salary.toLocaleString()}</td>
                  <td>{emp.email}</td>
                  <td className="actions">
                    <Link to={`/employees/${emp.id}/edit`} className="btn btn-sm">
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(emp.id)}
                      className="btn btn-sm btn-danger"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {employees.length === 0 && <p className="empty">No employees found.</p>}

          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="btn btn-sm"
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Previous
              </button>
              <span className="page-info">
                Page {page} of {totalPages}
              </span>
              <button
                className="btn btn-sm"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
