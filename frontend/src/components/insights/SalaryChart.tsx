"use client";

import {
	BarChart,
	Bar,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	ResponsiveContainer,
} from "recharts";

interface Props {
	data: { label: string; avg: number }[];
	title: string;
}

function formatK(v: number) {
	return v >= 1000 ? `$${(v / 1000).toFixed(0)}k` : `$${v}`;
}

export function SalaryChart({ data, title }: Props) {
	return (
		<div className="rounded-lg border border-zinc-200 bg-white p-5">
			<h2 className="mb-4 text-sm font-semibold text-zinc-900">{title}</h2>
			{data.length === 0 ? (
				<div className="flex h-52 items-center justify-center text-sm text-zinc-400">
					No data available
				</div>
			) : (
				<ResponsiveContainer width="100%" height={220}>
					<BarChart data={data} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#f4f4f5" vertical={false} />
						<XAxis
							dataKey="label"
							tick={{ fontSize: 11, fill: "#71717a" }}
							axisLine={false}
							tickLine={false}
						/>
						<YAxis
							tickFormatter={formatK}
							tick={{ fontSize: 11, fill: "#71717a" }}
							axisLine={false}
							tickLine={false}
							width={40}
						/>
						<Tooltip
							formatter={(v) =>
								new Intl.NumberFormat("en-US", {
									style: "currency",
									currency: "USD",
									maximumFractionDigits: 0,
								}).format(Number(v))
							}
							contentStyle={{
								fontSize: 12,
								border: "1px solid #e4e4e7",
								borderRadius: 6,
								boxShadow: "none",
							}}
							cursor={{ fill: "#f4f4f5" }}
						/>
						<Bar dataKey="avg" fill="#18181b" radius={[3, 3, 0, 0]} maxBarSize={40} />
					</BarChart>
				</ResponsiveContainer>
			)}
		</div>
	);
}
