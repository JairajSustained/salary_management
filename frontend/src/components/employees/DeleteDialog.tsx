"use client";

import { useState } from "react";
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

	const handleDelete = async () => {
		if (!employee) return;
		setIsDeleting(true);
		try {
			await employeesApi.delete(employee.id);
			onSuccess();
			onClose();
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
