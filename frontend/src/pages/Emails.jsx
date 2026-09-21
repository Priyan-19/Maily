import { useEffect, useState } from "react"

import EmailCard from "../components/EmailCard"
import {
    getEmails,
    syncEmails,
} from "../services/api"

function Emails() {
    const [emails, setEmails] = useState([])
    const [loading, setLoading] = useState(true)
    const [syncing, setSyncing] = useState(false)
    const [error, setError] = useState("")

    const loadEmails = async () => {
        try {
            setLoading(true)

            const data = await getEmails()

            setEmails(data.emails || [])
            setError("")
        } catch (error) {
            console.error(error)
            setError("Failed to load emails.")
        } finally {
            setLoading(false)
        }
    }

    const handleSync = async () => {
        try {
            setSyncing(true)
            setError("")

            await syncEmails()
            await loadEmails()
        } catch (error) {
            console.error(error)
            setError("Failed to sync Gmail.")
        } finally {
            setSyncing(false)
        }
    }

    useEffect(() => {
        loadEmails()
    }, [])

    if (loading) {
        return (
            <div className="flex min-h-40 items-center justify-center">
                <p className="text-slate-500">
                    Loading emails...
                </p>
            </div>
        )
    }

    return (
        <div>
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold">
                        Emails
                    </h1>

                    <p className="mt-1 text-slate-500">
                        Your emails and AI analysis.
                    </p>
                </div>

                <button
                    onClick={handleSync}
                    disabled={syncing}
                    className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
                >
                    {syncing ? "Syncing..." : "Sync Gmail"}
                </button>
            </div>

            {error && (
                <div className="mb-5 rounded-lg bg-red-50 p-4 text-sm text-red-600">
                    {error}
                </div>
            )}

            {emails.length === 0 ? (
                <div className="rounded-xl border border-slate-200 bg-white p-10 text-center">
                    <p className="text-slate-500">
                        No emails found.
                    </p>
                </div>
            ) : (
                <div className="grid gap-4 md:grid-cols-2">
                    {emails.map((email) => (
                        <EmailCard
                            key={email.id}
                            email={email}
                        />
                    ))}
                </div>
            )}
        </div>
    )
}

export default Emails