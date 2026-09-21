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
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-start justify-between gap-4">
                    <div>
                        <h1 className="text-2xl font-bold text-slate-900">{email.subject || "(No Subject)"}</h1>
                        <p className="mt-2 text-sm text-slate-500">From: {email.sender}</p>
                    </div>

                    <PriorityBadge importance={analysis?.importance} />
                </div>

                <div className="mt-6 whitespace-pre-wrap text-sm leading-7 text-slate-700 border-t border-slate-100 pt-4">
                    {email.body || email.snippet}
                </div>
            </div>

            {analysis && (
                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-bold text-slate-900">AI Intelligence & Summary</h2>

                    <p className="mt-4 text-slate-700 text-sm leading-6 bg-slate-50 p-4 rounded-lg border border-slate-200">
                        {analysis.summary}
                    </p>

                    <div className="mt-4 flex flex-wrap gap-2">
                        <span className="rounded-md bg-indigo-50 text-indigo-700 px-3 py-1 text-xs font-semibold uppercase tracking-wider">
                            Language: {analysis.language}
                        </span>

                        <span className="rounded-md bg-slate-100 text-slate-700 px-3 py-1 text-xs font-semibold uppercase tracking-wider">
                            Category: {analysis.category}
                        </span>
                    </div>

                    {analysis.actions?.length > 0 && (
                        <div className="mt-6">
                            <h3 className="mb-3 font-semibold text-slate-900">Required Actions</h3>
                            <div className="space-y-2">
                                {analysis.actions.map((action, index) => (
                                    <ActionCard key={index} action={action} />
                                ))}
                            </div>
                        </div>
                    )}

                    {analysis.deadlines?.length > 0 && (
                        <div className="mt-6">
                            <h3 className="mb-3 font-semibold text-slate-900">Deadlines</h3>
                            <ul className="space-y-2 text-sm">
                                {analysis.deadlines.map((deadline, index) => (
                                    <li key={index} className="rounded-lg bg-amber-50 border border-amber-200 p-3 text-amber-800 font-medium">
                                        Deadline: {deadline}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}

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