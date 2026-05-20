"use client";

import { useState } from "react";
import { isAxiosError } from "axios";
import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
} from "@/components/ui/dialog";
import { EmployeeForm } from "./EmployeeForm";
import { employeesApi } from "@/lib/api";
import type { Employee, EmployeeFormData } from "@/types/employee";

interface Props {
	open: boolean;
	onClose: () => void;
	employee?: Employee;
	onSuccess: () => void;
}

export function EmployeeModal({ open, onClose, employee, onSuccess }: Props) {
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [genericError, setGenericError] = useState<string | null>(null);
	const [fieldErrors, setFieldErrors] = useState<Record<string, string[]> | undefined>();

	const handleSubmit = async (data: EmployeeFormData) => {
		setIsSubmitting(true);
		setGenericError(null);
		setFieldErrors(undefined);
		try {
			if (employee) {
				await employeesApi.update(employee.id, data);
			} else {
				await employeesApi.create(data);
			}
			onSuccess();
			onClose();
		} catch (err) {
			if (isAxiosError(err) && err.response?.data) {
				const data = err.response.data as Record<string, string | string[]>;
				// Separate field errors from non-field errors (e.g. "non_field_errors", "detail")
				const fieldErrs: Record<string, string[]> = {};
				const topLevelMessages: string[] = [];
				for (const [key, val] of Object.entries(data)) {
					if (key === "non_field_errors" || key === "detail") {
						topLevelMessages.push(Array.isArray(val) ? val.join(" ") : val);
					} else {
						fieldErrs[key] = Array.isArray(val) ? val : [val];
					}
				}
				if (Object.keys(fieldErrs).length) setFieldErrors(fieldErrs);
				if (topLevelMessages.length) setGenericError(topLevelMessages.join(" "));
			} else {
				setGenericError("Something went wrong. Please try again.");
			}
		} finally {
			setIsSubmitting(false);
		}
	};

	return (
		<Dialog open={open} onOpenChange={(o) => !o && onClose()}>
			<DialogContent className="max-w-lg">
				<DialogHeader>
					<DialogTitle>
						{employee ? "Edit Employee" : "Add Employee"}
					</DialogTitle>
				</DialogHeader>
				{genericError && (
					<p className="rounded bg-red-50 px-3 py-2 text-sm text-red-600">
						{genericError}
					</p>
				)}
				<EmployeeForm
					defaultValues={employee}
					onSubmit={handleSubmit}
					isSubmitting={isSubmitting}
					fieldErrors={fieldErrors}
				/>
			</DialogContent>
		</Dialog>
	);
}
