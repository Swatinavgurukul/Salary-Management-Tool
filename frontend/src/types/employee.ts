export interface Employee {
  id: number;
  full_name: string;
  job_title: string;
  country: string;
  salary: number;
  department: string;
  email: string;
  created_at: string | null;
  updated_at: string | null;
}

export interface EmployeeCreate {
  full_name: string;
  job_title: string;
  country: string;
  salary: number;
  department: string;
  email: string;
}

export interface EmployeeUpdate {
  full_name?: string;
  job_title?: string;
  country?: string;
  salary?: number;
  department?: string;
  email?: string;
}

export interface CountryInsight {
  country: string;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  employee_count: number;
}

export interface JobInsight {
  job_title: string;
  country?: string;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  employee_count: number;
}
