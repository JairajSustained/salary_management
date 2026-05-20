"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import type { Employee, EmployeeFormData } from "@/types/employee";

interface Props {
	defaultValues?: Employee;
	onSubmit: (data: EmployeeFormData) => Promise<void>;
	isSubmitting: boolean;
	fieldErrors?: Record<string, string[]>;
}

const DEPARTMENTS = [
	"Engineering", "Product", "Design", "Data", "HR",
	"Finance", "Marketing", "Sales", "Operations", "Legal",
	"Security", "Customer Success",
];

const COUNTRIES = [
	"USA", "India", "UK", "Canada", "Germany", "France", "Australia",
	"Brazil", "Netherlands", "Singapore", "Japan", "Spain", "Sweden",
	"Poland", "Mexico", "Italy", "South Korea", "Switzerland", "UAE", "Portugal",
];

export function EmployeeForm({ defaultValues, onSubmit, isSubmitting, fieldErrors }: Props) {
	const {
		register,
		handleSubmit,
		setValue,
		watch,
		reset,
		setError,
		formState: { errors },
	} = useForm<EmployeeFormData>({
		defaultValues: defaultValues
			? {
					first_name: defaultValues.first_name,
					last_name: defaultValues.last_name,
					job_title: defaultValues.job_title,
					department: defaultValues.department,
					country: defaultValues.country,
					salary: defaultValues.salary,
					date_of_joining: defaultValues.date_of_joining,
					employment_status: defaultValues.employment_status,
				}
			: { employment_status: "Active" },
	});

	useEffect(() => {
		if (defaultValues) reset({
			first_name: defaultValues.first_name,
			last_name: defaultValues.last_name,
			job_title: defaultValues.job_title,
			department: defaultValues.department,
			country: defaultValues.country,
			salary: defaultValues.salary,
			date_of_joining: defaultValues.date_of_joining,
			employment_status: defaultValues.employment_status,
		});
	}, [defaultValues, reset]);

	useEffect(() => {
		if (!fieldErrors) return;
		(Object.entries(fieldErrors) as [keyof EmployeeFormData, string[]][]).forEach(
			([field, messages]) => setError(field, { message: messages[0] })
		);
	}, [fieldErrors, setError]);

	return (
		<form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
			<div className="grid grid-cols-2 gap-4">
				<div className="space-y-1.5">
					<Label htmlFor="first_name">First Name</Label>
					<Input
						id="first_name"
						{...register("first_name", { required: "Required" })}
						placeholder="Alice"
					/>
					{errors.first_name && (
						<p className="text-xs text-red-500">{errors.first_name.message}</p>
					)}
				</div>
				<div className="space-y-1.5">
					<Label htmlFor="last_name">Last Name</Label>
					<Input
						id="last_name"
						{...register("last_name", { required: "Required" })}
						placeholder="Smith"
					/>
					{errors.last_name && (
						<p className="text-xs text-red-500">{errors.last_name.message}</p>
					)}
				</div>
			</div>

			<div className="space-y-1.5">
				<Label htmlFor="job_title">Job Title</Label>
				<Input
					id="job_title"
					{...register("job_title", { required: "Required" })}
					placeholder="Software Engineer"
				/>
				{errors.job_title && (
					<p className="text-xs text-red-500">{errors.job_title.message}</p>
				)}
			</div>

			<div className="grid grid-cols-2 gap-4">
				<div className="space-y-1.5">
					<Label>Department</Label>
					<Select
						value={watch("department") ?? ""}
						onValueChange={(v) => setValue("department", v as string)}
					>
						<SelectTrigger>
							<SelectValue placeholder="Select department" />
						</SelectTrigger>
						<SelectContent>
							{DEPARTMENTS.map((d) => (
								<SelectItem key={d} value={d}>{d}</SelectItem>
							))}
						</SelectContent>
					</Select>
				</div>
				<div className="space-y-1.5">
					<Label>Country</Label>
					<Select
						value={watch("country") ?? ""}
						onValueChange={(v) => setValue("country", v as string)}
					>
						<SelectTrigger>
							<SelectValue placeholder="Select country" />
						</SelectTrigger>
						<SelectContent>
							{COUNTRIES.map((c) => (
								<SelectItem key={c} value={c}>{c}</SelectItem>
							))}
						</SelectContent>
					</Select>
				</div>
			</div>

			<div className="grid grid-cols-2 gap-4">
				<div className="space-y-1.5">
					<Label htmlFor="salary">Salary (USD)</Label>
					<Input
						id="salary"
						type="number"
						{...register("salary", { required: "Required", min: { value: 1, message: "Must be > 0" } })}
						placeholder="75000"
					/>
					{errors.salary && (
						<p className="text-xs text-red-500">{errors.salary.message}</p>
					)}
				</div>
				<div className="space-y-1.5">
					<Label htmlFor="date_of_joining">Date of Joining</Label>
					<Input
						id="date_of_joining"
						type="date"
						{...register("date_of_joining", { required: "Required" })}
					/>
					{errors.date_of_joining && (
						<p className="text-xs text-red-500">{errors.date_of_joining.message}</p>
					)}
				</div>
			</div>

			<div className="space-y-1.5">
				<Label>Status</Label>
				<Select
					value={watch("employment_status") ?? ""}
					onValueChange={(v) => setValue("employment_status", v as "Active" | "Inactive")}
				>
					<SelectTrigger>
						<SelectValue />
					</SelectTrigger>
					<SelectContent>
						<SelectItem value="Active">Active</SelectItem>
						<SelectItem value="Inactive">Inactive</SelectItem>
					</SelectContent>
				</Select>
			</div>

			<Button type="submit" disabled={isSubmitting} className="w-full">
				{isSubmitting ? "Saving…" : defaultValues ? "Save Changes" : "Add Employee"}
			</Button>
		</form>
	);
}
