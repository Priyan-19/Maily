import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { getTodayDigest, generateDigest, syncEmails, getBriefing } from "../services/api"
import DigestCard from "../components/DigestCard"

function Dashboard() {
    const [digest, setDigest] = useState(null)
    const [briefing, setBriefing] = useState(null)
    const [activeTab, setActiveTab] = useState("must_read") // 'must_read', 'unread', 'last20', 'workflow'
    const [loading, setLoading] = useState(true)
    const [syncing, setSyncing] = useState(false)
    const [statusMsg, setStatusMsg] = useState("")

    const [connectNeeded, setConnectNeeded] = useState(false)

    const loadData = async () => {
        try {
            setLoading(true)
            const [digestData, briefingData] = await Promise.all([
                getTodayDigest(),
                getBriefing(),
            ])
            setDigest(digestData)
            setBriefing(briefingData)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const refreshDigest = async () => {
        try {
            setLoading(true)
            setStatusMsg("Refreshing AI Intelligence...")
            const data = await generateDigest()
            setDigest(data)
            const bData = await getBriefing()
            setBriefing(bData)
            setStatusMsg("AI Intelligence updated!")
            setTimeout(() => setStatusMsg(""), 3000)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleSync = async () => {
        try {
            setSyncing(true)
            setConnectNeeded(false)
            setStatusMsg("Syncing Gmail Primary emails...")
            await syncEmails()
            await refreshDigest()
            setStatusMsg("Gmail sync completed successfully!")
            setTimeout(() => setStatusMsg(""), 4000)
        } catch (err) {
            console.error(err)
            const detail = err.response?.data?.detail || "Sync failed. No Gmail account connected."
            setStatusMsg(detail)
            setConnectNeeded(true)
        } finally {
            setSyncing(false)
        }
    }

    useEffect(() => {
        const queryParams = new URLSearchParams(window.location.search)
        if (queryParams.get("auth") === "success") {
            window.history.replaceState({}, document.title, window.location.pathname)
            setStatusMsg("Google Auth successful! Syncing Gmail emails...")
            handleSync()
        } else {
            loadData()
        }
    }, [])

    if (loading && !digest) {
        return (
            <div className="p-12 text-center text-slate-500">
                <img src="/robot.png" alt="Loading Robot" className="w-16 h-16 mx-auto animate-float-robot mb-3 object-contain" />
                <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-r-transparent" />
                <p className="mt-4 text-base font-semibold text-slate-700">Loading AI Executive Briefing & Context...</p>
            </div>
        )
    }

    return (
        <div className="space-y-8">
            {/* Header section */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">
                        Executive AI Briefing
                    </h1>
                    <p className="mt-1 text-sm text-slate-500 font-medium">
                        Instant email intelligence, unread alerts, and automated tool-calling workflow.
                    </p>
                </div>

                <div className="flex flex-wrap items-center gap-3">
                    <a
                        href="http://127.0.0.1:8000/api/auth/google"
                        className="rounded-xl bg-white border border-red-200 text-red-600 hover:bg-red-50 px-4 py-2.5 text-sm font-semibold shadow-sm transition flex items-center gap-2"
                    >
                        <svg className="w-4 h-4 text-red-500 fill-current" viewBox="0 0 24 24">
                            <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032 s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2 C6.721,2,2,6.721,2,12.545S6.721,23.09,12.545,23.09c6.627,0,11.026-4.656,11.026-11.226c0-0.665-0.066-1.165-0.165-1.625H12.545z" />
                        </svg>
                        Connect Gmail
                    </a>

                    <button
                        onClick={handleSync}
                        disabled={syncing}
                        className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50 transition disabled:opacity-50 flex items-center gap-2"
                    >
                        <svg className={`w-4 h-4 text-indigo-600 ${syncing ? "animate-spin" : ""}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        {syncing ? "Syncing..." : "Sync Gmail"}
                    </button>

                    <button
                        onClick={refreshDigest}
                        className="rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-indigo-200 hover:bg-indigo-700 transition"
                    >
                        Refresh Briefing
                    </button>
                </div>
            </div>

            {statusMsg && (
                <div className={`rounded-xl p-4 text-sm font-semibold border flex items-center justify-between gap-4 animate-fade-in ${connectNeeded ? "bg-amber-50 border-amber-300 text-amber-900" : "bg-indigo-50 border-indigo-200 text-indigo-800"}`}>
                    <div>{statusMsg}</div>
                    {connectNeeded && (
                        <a
                            href="http://127.0.0.1:8000/api/auth/google"
                            className="rounded-lg bg-red-600 px-3 py-1.5 text-xs font-bold text-white shadow-sm hover:bg-red-700 transition flex-shrink-0"
                        >
                            Log in with Google OAuth ➔
                        </a>
                    )}
                </div>
            )}

            {/* AI Executive Audio/Narrative Briefing Banner */}
            <div className="rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 md:p-8 text-white shadow-xl shadow-indigo-950/20 relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="absolute right-0 top-0 opacity-10 translate-x-12 -translate-y-8">
                    <svg className="w-96 h-96" fill="currentColor" viewBox="0 0 200 200">
                        <path d="M45,-62C58.3,-53.1,69.2,-40.4,74.5,-25.6C79.8,-10.8,79.5,6.1,74.1,21.5C68.7,36.9,58.2,50.8,44.7,60.2C31.2,69.6,14.6,74.5,-1.3,76.3C-17.2,78.1,-34.4,76.8,-47.4,68C-60.4,59.2,-69.2,42.9,-73.4,25.8C-77.6,8.7,-77.2,-9.2,-70.7,-24.1C-64.2,-39,-51.6,-50.9,-38.1,-59.7C-24.6,-68.5,-10.2,-74.2,3.3,-78.8C16.8,-83.4,31.7,-70.9,45,-62Z" transform="translate(100 100)" />
                    </svg>
                </div>

                <div className="relative z-10 flex-1 space-y-4">
                    <div className="flex items-center gap-3">
                        <span className="rounded-full bg-indigo-500/30 border border-indigo-400/40 px-3 py-1 text-xs font-bold uppercase tracking-wider text-indigo-300">
                            Instant Context Summary ({briefing?.user_language || "Tanglish"})
                        </span>
                        <span className="text-xs text-slate-300 font-medium">Real-time LLM Synthesis</span>
                    </div>

                    <p className="text-xl md:text-2xl font-bold leading-relaxed text-indigo-50">
                        "{briefing?.executive_briefing}"
                    </p>

                    <div className="flex flex-wrap items-center gap-6 pt-2">
                        <div className="flex items-center gap-2">
                            <div className="h-3 w-3 rounded-full bg-red-400 animate-ping" />
                            <span className="text-sm font-semibold text-slate-200">
                                Must-Read: <strong className="text-white text-lg">{briefing?.must_read_count || 0}</strong>
                            </span>
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="h-3 w-3 rounded-full bg-amber-400" />
                            <span className="text-sm font-semibold text-slate-200">
                                Unread: <strong className="text-white text-lg">{briefing?.unread_count || 0}</strong>
                            </span>
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="h-3 w-3 rounded-full bg-emerald-400" />
                            <span className="text-sm font-semibold text-slate-200">
                                Total Analyzed: <strong className="text-white text-lg">{briefing?.total_recent || 0}</strong>
                            </span>
                        </div>
                    </div>
                </div>

                <div className="relative z-10 flex-shrink-0 flex flex-col items-center">
                    <div className="relative">
                        <img
                            src="/robot.png"
                            alt="Robot Mascot Assistant"
                            className="w-28 h-28 md:w-36 md:h-36 object-contain animate-float-robot drop-shadow-[0_20px_25px_rgba(0,0,0,0.5)]"
                        />
                        <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-20 h-3 bg-black/40 rounded-full blur-xs animate-pulse" />
                    </div>
                    <span className="mt-2 text-xs font-bold text-indigo-300 bg-indigo-900/60 px-3 py-1 rounded-full border border-indigo-700/50">
                        Maily Robot AI
                    </span>
                </div>
            </div>

            {/* Interactive Category Tabs */}
            <div className="flex border-b border-slate-200 space-x-6 text-sm font-bold">
                <button
                    onClick={() => setActiveTab("must_read")}
                    className={`pb-3 border-b-2 transition ${activeTab === "must_read" ? "border-indigo-600 text-indigo-600" : "border-transparent text-slate-500 hover:text-slate-900"}`}
                >
                    Must-Read Emails ({briefing?.must_read_emails?.length || 0})
                </button>

                <button
                    onClick={() => setActiveTab("unread")}
                    className={`pb-3 border-b-2 transition ${activeTab === "unread" ? "border-indigo-600 text-indigo-600" : "border-transparent text-slate-500 hover:text-slate-900"}`}
                >
                    Unread Inbox ({briefing?.unread_emails?.length || 0})
                </button>

                <button
                    onClick={() => setActiveTab("last20")}
                    className={`pb-3 border-b-2 transition ${activeTab === "last20" ? "border-indigo-600 text-indigo-600" : "border-transparent text-slate-500 hover:text-slate-900"}`}
                >
                    Last 20 Emails Context ({briefing?.last_20_emails?.length || 0})
                </button>

                <button
                    onClick={() => setActiveTab("workflow")}
                    className={`pb-3 border-b-2 transition ${activeTab === "workflow" ? "border-indigo-600 text-indigo-600" : "border-transparent text-slate-500 hover:text-slate-900"}`}
                >
                    AI Tool Agent Workflow Diagram
                </button>
            </div>

            {/* Tab 1: Must Read */}
            {activeTab === "must_read" && (
                <div className="space-y-4">
                    {briefing?.must_read_emails?.length > 0 ? (
                        briefing.must_read_emails.map((item) => (
                            <div key={item.id} className="rounded-2xl border border-red-200/80 bg-red-50/20 p-5 shadow-sm hover:border-red-300 transition">
                                <div className="flex items-start justify-between gap-4">
                                    <div>
                                        <Link to={`/emails/${item.id}`} className="font-bold text-slate-900 hover:text-indigo-600 text-base">
                                            {item.subject}
                                        </Link>
                                        <p className="text-xs text-slate-500 mt-1">{item.sender}</p>
                                    </div>

                                    <span className="rounded-md bg-red-100 text-red-700 px-2.5 py-1 text-xs font-extrabold uppercase">
                                        Action Required
                                    </span>
                                </div>

                                <p className="mt-3 text-sm text-slate-700 leading-6 bg-white p-3 rounded-xl border border-slate-200/60">
                                    {item.summary}
                                </p>

                                {item.actions?.length > 0 && (
                                    <div className="mt-3">
                                        <p className="text-xs font-bold text-indigo-600 uppercase tracking-wider mb-1">Actions to Take:</p>
                                        <ul className="text-xs font-medium text-slate-700 space-y-1">
                                            {item.actions.map((act, i) => (
                                                <li key={i} className="flex items-center gap-1.5">
                                                    <span className="text-indigo-600">✓</span> {act}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        ))
                    ) : (
                        <div className="rounded-2xl bg-white p-12 text-center text-slate-500 border border-slate-200">
                            No urgent action emails pending right now.
                        </div>
                    )}
                </div>
            )}

            {/* Tab 2: Unread */}
            {activeTab === "unread" && (
                <div className="space-y-4">
                    {briefing?.unread_emails?.length > 0 ? (
                        briefing.unread_emails.map((item) => (
                            <div key={item.id} className="rounded-2xl border border-amber-200/80 bg-amber-50/20 p-5 shadow-sm hover:border-amber-300 transition">
                                <div className="flex items-start justify-between gap-4">
                                    <div>
                                        <Link to={`/emails/${item.id}`} className="font-bold text-slate-900 hover:text-indigo-600 text-base">
                                            {item.subject}
                                        </Link>
                                        <p className="text-xs text-slate-500 mt-1">{item.sender}</p>
                                    </div>

                                    <span className="rounded-md bg-amber-100 text-amber-800 px-2.5 py-1 text-xs font-bold uppercase">
                                        Unread
                                    </span>
                                </div>

                                <p className="mt-3 text-sm text-slate-700 leading-6">
                                    {item.summary || item.snippet}
                                </p>
                            </div>
                        ))
                    ) : (
                        <div className="rounded-2xl bg-white p-12 text-center text-slate-500 border border-slate-200">
                            You are all caught up! No unread emails in Primary inbox.
                        </div>
                    )}
                </div>
            )}

            {/* Tab 3: Last 20 Emails Context */}
            {activeTab === "last20" && (
                <div className="space-y-4">
                    {briefing?.last_20_emails?.map((item) => (
                        <div key={item.id} className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm hover:border-indigo-200 transition">
                            <div className="flex items-start justify-between gap-4">
                                <div>
                                    <Link to={`/emails/${item.id}`} className="font-bold text-slate-900 hover:text-indigo-600 text-base">
                                        {item.subject}
                                    </Link>
                                    <p className="text-xs text-slate-500 mt-1">{item.sender}</p>
                                </div>
                                <span className="text-xs font-medium text-slate-400">
                                    {item.received_at ? new Date(item.received_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                                </span>
                            </div>

                            <p className="mt-3 text-sm text-slate-600 leading-6 bg-slate-50/60 p-3 rounded-xl border border-slate-100">
                                {item.summary}
                            </p>
                        </div>
                    ))}
                </div>
            )}

            {/* Tab 4: Interactive AI Tool Workflow Diagram */}
            {activeTab === "workflow" && (
                <div className="rounded-3xl border border-slate-800 bg-slate-950 p-8 text-white shadow-2xl space-y-6">
                    <div>
                        <span className="rounded-full bg-indigo-500/20 border border-indigo-500/40 px-3 py-1 text-xs font-bold uppercase tracking-wider text-indigo-400">
                            System Flow Visualizer
                        </span>
                        <h2 className="text-2xl font-bold mt-2 text-white">AI Tool-Calling Workflow Execution</h2>
                        <p className="text-sm text-slate-400 mt-1">
                            Live visualization of Maily's multi-step LLM routing, classification, tool execution, and Gmail draft creation.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-5 gap-4 items-center pt-4">
                        <div className="rounded-2xl border border-indigo-500/40 bg-indigo-950/50 p-4 text-center space-y-2">
                            <div className="w-10 h-10 mx-auto rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-300 font-bold text-sm">
                                1
                            </div>
                            <p className="text-xs font-bold text-indigo-300">Trigger</p>
                            <p className="text-xs text-slate-300">Gmail Primary OAuth Fetch</p>
                        </div>

                        <div className="text-center text-slate-500 hidden md:block">➔</div>

                        <div className="rounded-2xl border border-purple-500/40 bg-purple-950/50 p-4 text-center space-y-2">
                            <div className="w-10 h-10 mx-auto rounded-full bg-purple-500/20 flex items-center justify-center text-purple-300 font-bold text-sm">
                                2
                            </div>
                            <p className="text-xs font-bold text-purple-300">LLM Analysis</p>
                            <p className="text-xs text-slate-300">Classifier & Action Extractor</p>
                        </div>

                        <div className="text-center text-slate-500 hidden md:block">➔</div>

                        <div className="rounded-2xl border border-emerald-500/40 bg-emerald-950/50 p-4 text-center space-y-2">
                            <div className="w-10 h-10 mx-auto rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-300 font-bold text-sm">
                                3
                            </div>
                            <p className="text-xs font-bold text-emerald-300">Tool Calling</p>
                            <p className="text-xs text-slate-300">Gmail Draft / Reminders / Digest</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Dashboard