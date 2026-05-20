import axios from "axios";
import type {
	Employee,
	EmployeeFormData,
	InsightsData,
	PaginatedEmployees,
} from "@/types/employee";

const client = axios.create({
	baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api",
	headers: { "Content-Type": "application/json" },
});

export const employeesApi = {
	list: (page = 1) =>
		client.get<PaginatedEmployees>(`/employees/?page=${page}`).then((r) => r.data),

	create: (data: EmployeeFormData) =>
		client.post<Employee>("/employees/", data).then((r) => r.data),

	retrieve: (id: string) =>
		client.get<Employee>(`/employees/${id}/`).then((r) => r.data),

	update: (id: string, data: Partial<EmployeeFormData>) =>
		client.patch<Employee>(`/employees/${id}/`, data).then((r) => r.data),

	delete: (id: string) => client.delete(`/employees/${id}/`),
};

export const insightsApi = {
	get: () => client.get<InsightsData>("/employees/insights/").then((r) => r.data),
};
