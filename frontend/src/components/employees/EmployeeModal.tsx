"use client";

import { useState } from "react";
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
	const [error, setError] = useState<string | null>(null);

	const handleSubmit = async (data: EmployeeFormData) => {
		setIsSubmitting(true);
		setError(null);
		try {
			if (employee) {
				await employeesApi.update(employee.id, data);
			} else {
				await employeesApi.create(data);
			}
			onSuccess();
			onClose();
		} catch {
			setError("Something went wrong. Please try again.");
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
				{error && (
					<p className="rounded bg-red-50 px-3 py-2 text-sm text-red-600">
						{error}
					</p>
				)}
				<EmployeeForm
					defaultValues={employee}
					onSubmit={handleSubmit}
					isSubmitting={isSubmitting}
				/>
			</DialogContent>
		</Dialog>
	);
}
