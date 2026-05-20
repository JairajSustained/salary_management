"use client";

import { Card, CardContent } from "@/components/ui/card";
import type { InsightsData } from "@/types/employee";

interface Props {
	data: InsightsData;
}

function avg(entries: { avg_salary: string }[]) {
	if (!entries.length) return 0;
	return entries.reduce((s, e) => s + Number(e.avg_salary), 0) / entries.length;
}

function formatUSD(n: number) {
	return new Intl.NumberFormat("en-US", {
		style: "currency",
		currency: "USD",
		maximumFractionDigits: 0,
	}).format(n);
}

export function SummaryCards({ data }: Props) {
	const allSalaries = [
		...data.by_country,
	];
	const globalMin = Math.min(...allSalaries.map((e) => Number(e.min_salary)));
	const globalMax = Math.max(...allSalaries.map((e) => Number(e.max_salary)));
	const globalAvg = avg(allSalaries);

	const cards = [
		{ label: "Countries", value: data.by_country.length },
		{ label: "Departments", value: data.by_department.length },
		{ label: "Job Titles", value: data.by_title.length },
		{ label: "Avg Salary", value: formatUSD(globalAvg) },
		{ label: "Min Salary", value: formatUSD(globalMin) },
		{ label: "Max Salary", value: formatUSD(globalMax) },
	];

	return (
		<div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
			{cards.map(({ label, value }) => (
				<Card key={label} className="border-zinc-200">
					<CardContent className="p-4">
						<p className="text-xs text-zinc-500">{label}</p>
						<p className="mt-1 text-lg font-semibold text-zinc-900">{value}</p>
					</CardContent>
				</Card>
			))}
		</div>
	);
}
