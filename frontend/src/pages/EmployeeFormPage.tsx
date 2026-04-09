import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import type { EmployeeCreate } from "../types/employee";
import { createEmployee, fetchEmployee, updateEmployee } from "../api/client";

const EMPTY_FORM: EmployeeCreate = {
  full_name: "",
  job_title: "",
  country: "",
  salary: 0,
  department: "",
  email: "",
};

export default function EmployeeFormPage() {
  const { id } = useParams<{ id: string }>();
  const isEdit = Boolean(id);
  const navigate = useNavigate();

  const [form, setForm] = useState<EmployeeCreate>(EMPTY_FORM);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isEdit && id) {
      fetchEmployee(Number(id))
        .then((emp) =>
          setForm({
            full_name: emp.full_name,
            job_title: emp.job_title,
            country: emp.country,
            salary: emp.salary,
            department: emp.department,
            email: emp.email,
          })
        )
        .catch(() => setError("Employee not found"));
    }
  }, [id, isEdit]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === "salary" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      if (isEdit && id) {
        await updateEmployee(Number(id), form);
      } else {
        await createEmployee(form);
      }
      navigate("/");
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      if (typeof detail === "string") {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map((d: any) => d.msg).join(", "));
      } else {
        setError("Something went wrong");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Edit Employee" : "Add Employee"}</h2>

      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit} className="employee-form">
        <label>
          Full Name
          <input
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Job Title
          <input
            name="job_title"
            value={form.job_title}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Department
          <input
            name="department"
            value={form.department}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Country
          <input
            name="country"
            value={form.country}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Salary
          <input
            name="salary"
            type="number"
            min="1"
            step="0.01"
            value={form.salary || ""}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Email
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </label>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? "Saving..." : isEdit ? "Update" : "Create"}
          </button>
          <button
            type="button"
            className="btn"
            onClick={() => navigate("/")}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
