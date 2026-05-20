export type EmploymentStatus = "Active" | "Inactive";

export interface Employee {
	id: string;
	first_name: string;
	last_name: string;
	job_title: string;
	department: string;
	country: string;
	salary: string;
	date_of_joining: string;
	employment_status: EmploymentStatus;
	full_name?: string;
}

export interface PaginatedEmployees {
	count: number;
	next: string | null;
	previous: string | null;
	results: Employee[];
}

export type EmployeeFormData = Omit<Employee, "id" | "full_name">;

export interface InsightEntry {
	min_salary: string;
	max_salary: string;
	avg_salary: string;
	median_salary: string;
}

export interface CountryInsight extends InsightEntry {
	country: string;
}

export interface DepartmentInsight extends InsightEntry {
	department: string;
}

export interface TitleInsight extends InsightEntry {
	job_title: string;
}

export interface InsightsData {
	by_country: CountryInsight[];
	by_department: DepartmentInsight[];
	by_title: TitleInsight[];
}
