import { Link } from "react-router-dom"
import PriorityBadge from "./PriorityBadge"

function DigestCard({ email }) {
    return (
        <div className="group rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all duration-200 hover:border-indigo-200 hover:shadow-md">
            <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                    <Link
                        to={`/emails/${email.email_id}`}
                        className="font-bold text-slate-900 group-hover:text-indigo-600 transition-colors text-base"
                    >
                        {email.subject || "(No Subject)"}
                    </Link>

                    <p className="mt-1 text-xs font-medium text-slate-500">
                        {email.sender}
                    </p>
                </div>

                <div className="flex items-center gap-2">
                    <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wider text-slate-600">
                        {email.category || "General"}
                    </span>
                    <PriorityBadge importance={email.importance} />
                </div>
            </div>

            <p className="mt-3 text-sm leading-6 text-slate-600 bg-slate-50/70 p-3.5 rounded-xl border border-slate-100">
                {email.summary}
            </p>

            {email.actions?.length > 0 && (
                <div className="mt-4 border-t border-slate-100 pt-3">
                    <p className="mb-2 text-xs font-bold uppercase tracking-wider text-indigo-600 flex items-center gap-1.5">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Actions Required
                    </p>

                    <ul className="space-y-1.5 text-sm font-medium text-slate-700">
                        {email.actions.map((action, index) => (
                            <li key={index} className="flex items-start gap-2">
                                <span className="text-indigo-500 font-bold">•</span>
                                <span>{action}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {email.deadlines?.length > 0 && (
                <div className="mt-3">
                    <p className="mb-1.5 text-xs font-bold uppercase tracking-wider text-amber-600 flex items-center gap-1.5">
                        Deadlines
                    </p>

                    <ul className="space-y-1 text-sm font-medium text-slate-700">
                        {email.deadlines.map((deadline, index) => (
                            <li key={index} className="inline-block rounded-md bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-800 border border-amber-200/60 mr-2">
                                {deadline}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    )
}

export default DigestCard