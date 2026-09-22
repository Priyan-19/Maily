import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import PriorityBadge from "../components/PriorityBadge"
import ActionCard from "../components/ActionCard"
import { getEmail, suggestReply, createDraft } from "../services/api"

function EmailDetails() {
    const { id } = useParams()

    const [email, setEmail] = useState(null)
    const [loading, setLoading] = useState(true)

    // Draft Reply State
    const [instructions, setInstructions] = useState("")
    const [replyText, setReplyText] = useState("")
    const [draftStatus, setDraftStatus] = useState("")
    const [generatingReply, setGeneratingReply] = useState(false)
    const [creatingDraft, setCreatingDraft] = useState(false)

    useEffect(() => {
        const loadEmail = async () => {
            try {
                const found = await getEmail(id)
                setEmail(found)
            } catch (error) {
                console.error(error)
            } finally {
                setLoading(false)
            }
        }

        loadEmail()
    }, [id])

    const handleGenerateReply = async () => {
        try {
            setGeneratingReply(true)
            setDraftStatus("")
            const res = await suggestReply(id, instructions)
            setReplyText(res.suggested_reply || "")
        } catch (err) {
            console.error("Failed to generate reply", err)
            setDraftStatus("Failed to generate AI reply.")
        } finally {
            setGeneratingReply(false)
        }
    }

    const handleCreateDraft = async () => {
        if (!replyText.strip && !replyText.trim()) {
            alert("Reply text is empty.")
            return
        }

        try {
            setCreatingDraft(true)
            setDraftStatus("Creating Gmail Draft...")
            await createDraft(id, replyText)
            setDraftStatus("Gmail Draft created successfully! Check your Gmail Drafts folder.")
        } catch (err) {
            console.error("Failed to create draft", err)
            setDraftStatus("Failed to create Gmail draft.")
        } finally {
            setCreatingDraft(false)
        }
    }

    if (loading) {
        return <p className="p-6 text-slate-500">Loading email...</p>
    }

    if (!email) {
        return <p className="p-6 text-red-600">Email not found.</p>
    }

    const analysis = email.analysis

    return (
        <div className="max-w-4xl space-y-6">
            {analysis && (
                <div className="rounded-2xl border border-indigo-200 bg-white p-6 shadow-xs space-y-4">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                        <div className="flex items-center gap-2">
                            <span className="text-xl">⚡</span>
                            <h2 className="text-lg font-bold text-slate-900">AI Intelligence Summary</h2>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-100 px-3 py-1 text-xs font-bold uppercase tracking-wider">
                                {analysis.language}
                            </span>
                            <span className="rounded-lg bg-slate-100 text-slate-800 border border-slate-200 px-3 py-1 text-xs font-bold uppercase tracking-wider">
                                {analysis.category}
                            </span>
                        </div>
                    </div>

                    <div className="rounded-xl bg-slate-50/90 border border-slate-200 p-4">
                        <p className="text-[15px] font-medium text-slate-900 leading-relaxed">
                            {analysis.summary}
                        </p>
                    </div>

                    {analysis.actions?.length > 0 && (
                        <div className="space-y-2 pt-2">
                            <h3 className="text-xs font-bold text-indigo-700 uppercase tracking-wider">🎯 Required Actions:</h3>
                            <div className="space-y-2">
                                {analysis.actions.map((action, index) => (
                                    <ActionCard key={index} action={action} />
                                ))}
                            </div>
                        </div>
                    )}

                    {analysis.deadlines?.length > 0 && (
                        <div className="space-y-2 pt-2">
                            <h3 className="text-xs font-bold text-amber-700 uppercase tracking-wider">📅 Deadlines & Dates:</h3>
                            <div className="flex flex-wrap gap-2">
                                {analysis.deadlines.map((deadline, index) => (
                                    <span key={index} className="inline-flex items-center gap-2 rounded-lg bg-amber-50 border border-amber-200 px-3 py-1.5 text-xs font-bold text-amber-900">
                                        <span>⏰</span> {deadline}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
                <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-4">
                    <div>
                        <h1 className="text-2xl font-bold text-slate-900">{email.subject || "(No Subject)"}</h1>
                        <p className="mt-1.5 text-xs font-semibold text-slate-500">From: <span className="text-slate-700">{email.sender}</span></p>
                    </div>

                    <PriorityBadge importance={analysis?.importance} />
                </div>

                <div className="whitespace-pre-wrap text-sm leading-relaxed text-slate-800 bg-slate-50/50 p-5 rounded-xl border border-slate-200/60 font-sans">
                    {(email.body || email.snippet || "").replace(/^>\s*/gm, '').replace(/\*/g, '')}
                </div>
            </div>

            {/* AI Action Agent: Draft Reply */}
            <div className="rounded-2xl border border-indigo-200 bg-indigo-50/40 p-6 shadow-sm">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                        <img src="/robot.png" alt="Robot Mascot" className="w-12 h-12 object-contain animate-float-robot" />
                        <div>
                            <h2 className="text-xl font-bold text-slate-900">
                                AI Action Agent — Reply Assistant
                            </h2>
                            <p className="mt-0.5 text-xs text-slate-600">
                                Generate an AI reply in your preferred language and create a draft in your Gmail account.
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={handleGenerateReply}
                        disabled={generatingReply}
                        className="rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 transition disabled:opacity-50 shadow-sm"
                    >
                        {generatingReply ? "Generating..." : "Generate AI Reply"}
                    </button>
                </div>

                <div className="mt-4">
                    <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                        Custom Instructions (Optional)
                    </label>
                    <input
                        type="text"
                        placeholder="e.g. Confirm attendance for 10 AM, ask for location..."
                        value={instructions}
                        onChange={(e) => setInstructions(e.target.value)}
                        className="w-full rounded-lg border border-slate-300 p-3 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                </div>

                {replyText && (
                    <div className="mt-5 space-y-4">
                        <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">
                            Suggested Email Reply (Editable)
                        </label>
                        <textarea
                            rows={6}
                            value={replyText}
                            onChange={(e) => setReplyText(e.target.value)}
                            className="w-full rounded-lg border border-slate-300 p-3 text-sm font-sans bg-white leading-6 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />

                        <div className="flex items-center justify-between">
                            <span className="text-xs text-slate-500">
                                Action requires user confirmation before sending/creating draft.
                            </span>

                            <button
                                onClick={handleCreateDraft}
                                disabled={creatingDraft}
                                className="rounded-lg bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700 transition shadow-sm disabled:opacity-50"
                            >
                                {creatingDraft ? "Creating Draft..." : "Create Gmail Draft"}
                            </button>
                        </div>
                    </div>
                )}

                {draftStatus && (
                    <div className="mt-4 rounded-lg bg-white border border-slate-200 p-3 text-sm font-medium text-slate-700">
                        {draftStatus}
                    </div>
                )}
            </div>
        </div>
    )
}

export default EmailDetails