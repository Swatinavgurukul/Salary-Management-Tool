import axios from "axios";
import type {
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
  CountryInsight,
  JobInsight,
} from "../types/employee";

const api = axios.create({ baseURL: "/api" });

export async function fetchEmployees(): Promise<Employee[]> {
  const { data } = await api.get<Employee[]>("/employees");
  return data;
}

export async function fetchEmployee(id: number): Promise<Employee> {
  const { data } = await api.get<Employee>(`/employees/${id}`);
  return data;
}

export async function createEmployee(
  payload: EmployeeCreate
): Promise<Employee> {
  const { data } = await api.post<Employee>("/employees", payload);
  return data;
}

export async function updateEmployee(
  id: number,
  payload: EmployeeUpdate
): Promise<Employee> {
  const { data } = await api.put<Employee>(`/employees/${id}`, payload);
  return data;
}

export async function deleteEmployee(id: number): Promise<void> {
  await api.delete(`/employees/${id}`);
}

export async function fetchCountryInsight(
  country: string
): Promise<CountryInsight> {
  const { data } = await api.get<CountryInsight>(
    `/insights/country/${encodeURIComponent(country)}`
  );
  return data;
}

export async function fetchJobInsight(
  jobTitle: string,
  country?: string
): Promise<JobInsight> {
  const params: Record<string, string> = { job_title: jobTitle };
  if (country) params.country = country;
  const { data } = await api.get<JobInsight>("/insights/job", { params });
  return data;
}
