import { useEffect, useState } from "react"
import { getSettings, updateSettings, clearAllEmails } from "../services/api"

function Settings() {
    const [language, setLanguage] = useState("Tanglish")
    const [digestEnabled, setDigestEnabled] = useState(true)
    const [digestTime, setDigestTime] = useState("08:00")
    const [status, setStatus] = useState("")
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadSettings = async () => {
            try {
                const data = await getSettings()
                setLanguage(data.language || "Tanglish")
                setDigestEnabled(data.digest_enabled !== false)
                setDigestTime(data.digest_time || "08:00")
            } catch (err) {
                console.error("Failed to load settings", err)
            } finally {
                setLoading(false)
            }
        }

        loadSettings()
    }, [])

    const handleSave = async (newLang, newEnabled, newTime) => {
        try {
            setStatus("Saving...")
            await updateSettings({
                language: newLang,
                digest_enabled: newEnabled,
                digest_time: newTime,
            })
            setStatus("Preferences saved successfully.")
            setTimeout(() => setStatus(""), 3000)
        } catch (err) {
            console.error("Failed to save settings", err)
            setStatus("Failed to save preferences.")
        }
    }

    const handleClearData = async () => {
        if (window.confirm("Are you sure you want to clear all stored email and digest data?")) {
            try {
                setStatus("Clearing data...")
                await clearAllEmails()
                setStatus("All stored email data deleted successfully.")
                setTimeout(() => setStatus(""), 3000)
            } catch (err) {
                console.error("Failed to clear data", err)
                setStatus("Failed to clear email data.")
            }
        }
    }

    if (loading) {
        return <div className="p-6 text-slate-500">Loading settings...</div>
    }

    return (
        <div className="max-w-2xl space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-slate-900">Settings</h1>
                <p className="mt-1 text-slate-500">Manage your Maily preferences and output options.</p>
            </div>

            {status && (
                <div className="rounded-lg bg-indigo-50 border border-indigo-200 p-4 text-sm font-medium text-indigo-700">
                    {status}
                </div>
            )}

            <div className="space-y-4">
                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                    <h2 className="font-semibold text-slate-900">Output Language</h2>
                    <p className="mt-1 text-sm text-slate-500">
                        AI will generate email summaries, action items, and suggested replies in this language.
                    </p>

                    <select
                        value={language}
                        onChange={(e) => {
                            setLanguage(e.target.value)
                            handleSave(e.target.value, digestEnabled, digestTime)
                        }}
                        className="mt-4 w-full rounded-lg border border-slate-300 p-3 bg-white font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                        <option value="Tanglish">Tanglish (Tamil in English Script)</option>
                        <option value="Tamil">Tamil (தமிழ்)</option>
                        <option value="English">English</option>
                        <option value="Hindi">Hindi (हिंदी)</option>
                        <option value="Telugu">Telugu (తెలుగు)</option>
                        <option value="Malayalam">Malayalam (മലയാളം)</option>
                        <option value="Kannada">Kannada (கன்னட / ಕನ್ನಡ)</option>
                    </select>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                    <h2 className="font-semibold text-slate-900">Daily Digest Scheduling</h2>
                    <p className="mt-1 text-sm text-slate-500">Configure daily automated digest generation.</p>

                    <label className="mt-4 flex items-center gap-3 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={digestEnabled}
                            onChange={(e) => {
                                setDigestEnabled(e.target.checked)
                                handleSave(language, e.target.checked, digestTime)
                            }}
                            className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                        />
                        <span className="text-sm font-medium text-slate-700">Enable daily automated digest</span>
                    </label>

                    {digestEnabled && (
                        <div className="mt-4">
                            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                                Preferred Digest Time
                            </label>
                            <input
                                type="time"
                                value={digestTime}
                                onChange={(e) => {
                                    setDigestTime(e.target.value)
                                    handleSave(language, digestEnabled, e.target.value)
                                }}
                                className="rounded-lg border border-slate-300 p-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>
                    )}
                </div>

                <div className="rounded-xl border border-red-200 bg-red-50/30 p-6">
                    <h2 className="font-semibold text-red-900">Data & Privacy Control</h2>
                    <p className="mt-1 text-sm text-slate-600">
                        Delete all stored email data, AI analyses, and digests from the local database.
                    </p>

                    <button
                        onClick={handleClearData}
                        className="mt-4 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-red-700 transition"
                    >
                        Clear Stored Email Data
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Settings