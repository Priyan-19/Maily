import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import ActionCard from "../components/ActionCard"
import { getEmails } from "../services/api"

function Actions() {
    const [actions, setActions] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadActions = async () => {
            try {
                const res = await getEmails()
                const emailsList = res.emails || []
                const extracted = []

                emailsList.forEach((email) => {
                    email.analysis?.actions?.forEach((action) => {
                        extracted.push({
                            emailId: email.id,
                            subject: email.subject,
                            sender: email.sender,
                            action,
                        })
                    })
                })

                setActions(extracted)
            } catch (error) {
                console.error(error)
            } finally {
                setLoading(false)
            }
        }

        loadActions()
    }, [])

    if (loading) {
        return <div className="p-8 text-center text-slate-500">Loading extracted action tasks...</div>
    }

    return (
        <div className="max-w-4xl space-y-6">
            <div>
                <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">
                    Extracted Action Items
                </h1>
                <p className="mt-1 text-sm text-slate-500 font-medium">
                    Tasks automatically detected from your incoming emails.
                </p>
            </div>

            <div className="space-y-4">
                {actions.length > 0 ? (
                    actions.map((item, index) => (
                        <div key={index} className="group rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm transition hover:border-indigo-200 hover:shadow-md">
                            <div className="flex items-center justify-between gap-4 mb-3">
                                <div>
                                    <Link to={`/emails/${item.emailId}`} className="text-xs font-bold text-indigo-600 hover:underline">
                                        {item.subject || "(No Subject)"}
                                    </Link>
                                    <p className="text-xs text-slate-400 font-medium">{item.sender}</p>
                                </div>

                                <Link
                                    to={`/emails/${item.emailId}`}
                                    className="rounded-lg bg-indigo-50 px-3 py-1.5 text-xs font-semibold text-indigo-700 hover:bg-indigo-100 transition"
                                >
                                    View Email →
                                </Link>
                            </div>

                            <ActionCard action={item.action} />
                        </div>
                    ))
                ) : (
                    <div className="rounded-2xl border border-slate-200/80 bg-white p-12 text-center text-slate-500">
                        No pending action items found in your emails.
                    </div>
                )}
            </div>
        </div>
    )
}

export default Actions