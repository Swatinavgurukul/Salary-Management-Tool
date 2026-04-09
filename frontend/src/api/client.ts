import axios from "axios";
import type {
  Employee,
  PaginatedResponse,
  EmployeeCreate,
  EmployeeUpdate,
  CountryInsight,
  JobInsight,
  DepartmentInsight,
  HeadcountEntry,
} from "../types/employee";

const api = axios.create({ baseURL: "/api" });

export async function fetchEmployees(
  page = 1,
  pageSize = 20,
  search?: string
): Promise<PaginatedResponse> {
  const params: Record<string, string | number> = { page, page_size: pageSize };
  if (search) params.search = search;
  const { data } = await api.get<PaginatedResponse>("/employees", { params });
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

export async function fetchDepartmentInsights(): Promise<DepartmentInsight[]> {
  const { data } = await api.get<DepartmentInsight[]>("/insights/department");
  return data;
}

export async function fetchHeadcount(): Promise<HeadcountEntry[]> {
  const { data } = await api.get<HeadcountEntry[]>("/insights/headcount");
  return data;
}

export async function fetchTopEarners(limit = 10): Promise<Employee[]> {
  const { data } = await api.get<Employee[]>("/insights/top-earners", {
    params: { limit },
  });
  return data;
}
