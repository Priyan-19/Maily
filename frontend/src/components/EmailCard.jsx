import { useNavigate } from "react-router-dom"
import PriorityBadge from "./PriorityBadge"

function EmailCard({ email }) {
    const navigate = useNavigate()
    const analysis = email.analysis

    return (
        <div
            onClick={() => navigate(`/emails/${email.id}`)}
            className="group cursor-pointer rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all duration-200 hover:border-indigo-200 hover:shadow-md"
        >
            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                    <h3 className="truncate font-bold text-slate-900 group-hover:text-indigo-600 transition-colors text-base">
                        {email.subject || "(No Subject)"}
                    </h3>

                    <p className="mt-1 truncate text-xs font-medium text-slate-500">
                        {email.sender}
                    </p>
                </div>

                <PriorityBadge
                    importance={analysis?.importance || "low"}
                />
            </div>

            <div className="mt-3.5 rounded-xl bg-slate-50 border border-slate-200 p-3.5">
                <p className="line-clamp-2 text-sm font-medium leading-relaxed text-slate-900">
                    {analysis?.summary || email.snippet || "Click to view full email and AI analysis."}
                </p>
            </div>

            <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3">
                <div className="flex items-center gap-2">
                    {analysis?.category && (
                        <span className="rounded-md bg-indigo-50 px-2.5 py-0.5 text-xs font-semibold text-indigo-700 uppercase tracking-wider">
                            {analysis.category}
                        </span>
                    )}

                    {analysis?.language && (
                        <span className="rounded-md bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-600">
                            {analysis.language}
                        </span>
                    )}
                </div>

                {analysis?.actions?.length > 0 && (
                    <span className="text-xs font-bold text-indigo-600 flex items-center gap-1">
                        <span>{analysis.actions.length} action{analysis.actions.length > 1 ? "s" : ""}</span>
                        <span>→</span>
                    </span>
                )}
            </div>
        </div>
    )
}

export default EmailCard