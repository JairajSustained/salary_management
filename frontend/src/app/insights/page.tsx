"use client";

import { useEffect, useState } from "react";
import { SalaryChart } from "@/components/insights/SalaryChart";
import { SummaryCards } from "@/components/insights/SummaryCards";
import { insightsApi } from "@/lib/api";
import type { InsightsData } from "@/types/employee";

function ChartSkeleton() {
  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-5">
      <div className="mb-4 h-4 w-40 animate-pulse rounded bg-zinc-100" />
      <div className="h-52 animate-pulse rounded bg-zinc-100" />
    </div>
  );
}

function CardSkeleton() {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="h-20 animate-pulse rounded-lg border border-zinc-200 bg-white" />
      ))}
    </div>
  );
}

export default function InsightsPage() {
  const [data, setData] = useState<InsightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    insightsApi
      .get()
      .then(setData)
      .catch(() => setError("Failed to load insights. Is the backend running?"))
      .finally(() => setLoading(false));
  }, []);

  const byCountry = (data?.by_country ?? []).map((e) => ({
    label: e.country,
    avg: Math.round(Number(e.avg_salary)),
  }));

  const byDepartment = (data?.by_department ?? []).map((e) => ({
    label: e.department,
    avg: Math.round(Number(e.avg_salary)),
  }));

  const byTitle = (data?.by_title ?? []).map((e) => ({
    label: e.job_title,
    avg: Math.round(Number(e.avg_salary)),
  }));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-zinc-900">Insights</h1>
        <p className="mt-0.5 text-sm text-zinc-500">
          Salary analytics across your organisation
        </p>
      </div>

      {error && (
        <p className="rounded bg-red-50 px-4 py-3 text-sm text-red-600">{error}</p>
      )}

      {loading ? (
        <>
          <CardSkeleton />
          <div className="grid gap-5 lg:grid-cols-2">
            <ChartSkeleton />
            <ChartSkeleton />
            <ChartSkeleton />
          </div>
        </>
      ) : data ? (
        <>
          <SummaryCards data={data} />
          <div className="grid gap-5 lg:grid-cols-2">
            <SalaryChart title="Avg Salary by Country" data={byCountry} />
            <SalaryChart title="Avg Salary by Department" data={byDepartment} />
            <div className="lg:col-span-2">
              <SalaryChart title="Avg Salary by Job Title" data={byTitle} />
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}
