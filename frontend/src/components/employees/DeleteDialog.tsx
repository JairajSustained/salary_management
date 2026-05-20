"use client";

import { useState } from "react";
import { isAxiosError } from "axios";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { employeesApi } from "@/lib/api";
import type { Employee } from "@/types/employee";

interface Props {
	employee: Employee | null;
	onClose: () => void;
	onSuccess: () => void;
}

export function DeleteDialog({ employee, onClose, onSuccess }: Props) {
	const [isDeleting, setIsDeleting] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const handleDelete = async () => {
		if (!employee) return;
		setIsDeleting(true);
		setError(null);
		try {
			await employeesApi.delete(employee.id);
			onSuccess();
			onClose();
		} catch (err) {
			if (isAxiosError(err) && err.response?.data) {
				const data = err.response.data as Record<string, string | string[]>;
				const detail = data["detail"] ?? data["non_field_errors"];
				if (detail) {
					setError(Array.isArray(detail) ? detail.join(" ") : detail);
				} else {
					setError("Failed to deactivate employee. Please try again.");
				}
			} else {
				setError("Something went wrong. Please try again.");
			}
		} finally {
			setIsDeleting(false);
		}
	};

	return (
		<AlertDialog open={!!employee} onOpenChange={(o) => !o && onClose()}>
			<AlertDialogContent>
				<AlertDialogHeader>
					<AlertDialogTitle>Deactivate employee?</AlertDialogTitle>
					<AlertDialogDescription>
						{employee?.first_name} {employee?.last_name} will be marked as Inactive.
						This can be undone by editing their record.
					</AlertDialogDescription>
				</AlertDialogHeader>
				{error && (
					<p className="rounded bg-red-50 px-3 py-2 text-sm text-red-600">{error}</p>
				)}
				<AlertDialogFooter>
					<AlertDialogCancel disabled={isDeleting}>Cancel</AlertDialogCancel>
					<AlertDialogAction
						onClick={handleDelete}
						disabled={isDeleting}
						className="bg-red-600 hover:bg-red-700 focus:ring-red-600"
					>
						{isDeleting ? "Deactivating…" : "Deactivate"}
					</AlertDialogAction>
				</AlertDialogFooter>
			</AlertDialogContent>
		</AlertDialog>
	);
}
