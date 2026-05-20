"use client";

import { useState, useCallback, useEffect } from "react";
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { EmployeeModal } from "./EmployeeModal";
import { DeleteDialog } from "./DeleteDialog";
import { employeesApi } from "@/lib/api";
import type { Employee, PaginatedEmployees } from "@/types/employee";

function formatSalary(s: string) {
	return new Intl.NumberFormat("en-US", {
		style: "currency",
		currency: "USD",
		maximumFractionDigits: 0,
	}).format(Number(s));
}

function TableSkeleton() {
	return (
		<>
			{Array.from({ length: 8 }).map((_, i) => (
				<TableRow key={i}>
					{Array.from({ length: 7 }).map((_, j) => (
						<TableCell key={j}>
							<div className="h-4 w-full animate-pulse rounded bg-zinc-100" />
						</TableCell>
					))}
					<TableCell>
						<div className="h-8 w-16 animate-pulse rounded bg-zinc-100" />
					</TableCell>
				</TableRow>
			))}
		</>
	);
}

function EmptyState({ onAdd }: { onAdd: () => void }) {
	return (
		<TableRow>
			<TableCell colSpan={8} className="py-20 text-center">
				<p className="text-sm font-medium text-zinc-900">No employees yet</p>
				<p className="mt-1 text-sm text-zinc-500">
					Get started by adding your first employee.
				</p>
				<Button onClick={onAdd} className="mt-4" size="sm">
					Add Employee
				</Button>
			</TableCell>
		</TableRow>
	);
}

export function EmployeeTable({ onAdd }: { onAdd: () => void }) {
	const [data, setData] = useState<PaginatedEmployees | null>(null);
	const [page, setPage] = useState(1);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [editTarget, setEditTarget] = useState<Employee | null>(null);
	const [deleteTarget, setDeleteTarget] = useState<Employee | null>(null);

	const load = useCallback(async (p: number) => {
		setLoading(true);
		setError(null);
		try {
			const result = await employeesApi.list(p);
			setData(result);
		} catch {
			setError("Failed to load employees. Is the backend running?");
		} finally {
			setLoading(false);
		}
	}, []);

	useEffect(() => { load(page); }, [page, load]);

	const refresh = () => load(page);

	const totalPages = data ? Math.ceil(data.count / 10) : 0;

	return (
		<>
			<div className="rounded-lg border border-zinc-200 bg-white">
				<Table>
					<TableHeader>
						<TableRow className="bg-zinc-50">
							<TableHead className="font-semibold text-zinc-700">Full Name</TableHead>
							<TableHead className="font-semibold text-zinc-700">Job Title</TableHead>
							<TableHead className="font-semibold text-zinc-700">Department</TableHead>
							<TableHead className="font-semibold text-zinc-700">Country</TableHead>
							<TableHead className="font-semibold text-zinc-700">Salary</TableHead>
							<TableHead className="font-semibold text-zinc-700">Status</TableHead>
							<TableHead className="font-semibold text-zinc-700">Joined</TableHead>
							<TableHead />
						</TableRow>
					</TableHeader>
					<TableBody>
						{error ? (
							<TableRow>
								<TableCell colSpan={8} className="py-12 text-center text-sm text-red-500">
									{error}
								</TableCell>
							</TableRow>
						) : loading ? (
							<TableSkeleton />
						) : !data || data.results.length === 0 ? (
							<EmptyState onAdd={onAdd} />
						) : (
							data.results.map((emp) => (
								<TableRow
									key={emp.id}
									className="cursor-pointer hover:bg-zinc-50"
									onClick={() => setEditTarget(emp)}
								>
									<TableCell className="font-medium text-zinc-900">
										{emp.first_name} {emp.last_name}
									</TableCell>
									<TableCell className="text-zinc-600">{emp.job_title}</TableCell>
									<TableCell className="text-zinc-600">{emp.department}</TableCell>
									<TableCell className="text-zinc-600">{emp.country}</TableCell>
									<TableCell className="text-zinc-600">{formatSalary(emp.salary)}</TableCell>
									<TableCell>
										<Badge
											variant={emp.employment_status === "Active" ? "default" : "secondary"}
											className={
												emp.employment_status === "Active"
													? "bg-emerald-50 text-emerald-700 hover:bg-emerald-50"
													: "bg-zinc-100 text-zinc-500"
											}
										>
											{emp.employment_status}
										</Badge>
									</TableCell>
									<TableCell className="text-zinc-600">
										{new Date(emp.date_of_joining).toLocaleDateString("en-GB", {
											day: "2-digit", month: "short", year: "numeric",
										})}
									</TableCell>
									<TableCell onClick={(e) => e.stopPropagation()}>
										{emp.employment_status === "Active" && (
											<Button
												variant="ghost"
												size="sm"
												className="text-red-500 hover:bg-red-50 hover:text-red-600"
												onClick={() => setDeleteTarget(emp)}
											>
												Deactivate
											</Button>
										)}
									</TableCell>
								</TableRow>
							))
						)}
					</TableBody>
				</Table>
			</div>

			{/* Pagination */}
			{data && data.count > 10 && (
				<div className="flex items-center justify-between text-sm text-zinc-500">
					<span>
						{data.count} employees · page {page} of {totalPages}
					</span>
					<div className="flex gap-2">
						<Button
							variant="outline"
							size="sm"
							disabled={!data.previous}
							onClick={() => setPage((p) => p - 1)}
						>
							Previous
						</Button>
						<Button
							variant="outline"
							size="sm"
							disabled={!data.next}
							onClick={() => setPage((p) => p + 1)}
						>
							Next
						</Button>
					</div>
				</div>
			)}

			<EmployeeModal
				open={!!editTarget}
				employee={editTarget ?? undefined}
				onClose={() => setEditTarget(null)}
				onSuccess={refresh}
			/>
			<DeleteDialog
				employee={deleteTarget}
				onClose={() => setDeleteTarget(null)}
				onSuccess={refresh}
			/>
		</>
	);
}
