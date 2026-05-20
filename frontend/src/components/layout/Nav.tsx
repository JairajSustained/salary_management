"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const links = [
	{ href: "/employees", label: "Employees" },
	{ href: "/insights", label: "Insights" },
];

export function Nav() {
	const pathname = usePathname();

	return (
		<header className="border-b border-zinc-200 bg-white">
			<div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-6">
				<span className="text-sm font-semibold tracking-tight text-zinc-900">
					SalaryMgr
				</span>
				<nav className="flex items-center gap-1">
					{links.map(({ href, label }) => (
						<Link
							key={href}
							href={href}
							className={cn(
								"rounded px-3 py-1.5 text-sm font-medium transition-colors",
								pathname.startsWith(href)
									? "bg-zinc-900 text-white"
									: "text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900"
							)}
						>
							{label}
						</Link>
					))}
				</nav>
			</div>
		</header>
	);
}
