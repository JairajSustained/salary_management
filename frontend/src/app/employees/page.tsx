"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { EmployeeTable } from "@/components/employees/EmployeeTable";
import { EmployeeModal } from "@/components/employees/EmployeeModal";

export default function EmployeesPage() {
  const [addOpen, setAddOpen] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = () => setRefreshKey((k) => k + 1);

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-zinc-900">Employees</h1>
          <p className="mt-0.5 text-sm text-zinc-500">
            Manage your organisation&apos;s workforce
          </p>
        </div>
        <Button onClick={() => setAddOpen(true)}>Add Employee</Button>
      </div>

      <EmployeeTable key={refreshKey} onAdd={() => setAddOpen(true)} />

      <EmployeeModal
        open={addOpen}
        onClose={() => setAddOpen(false)}
        onSuccess={refresh}
      />
    </div>
  );
}
