function ActionCard({ action }) {
    return (
        <div className="flex items-start gap-3 rounded-lg border border-slate-200 bg-white p-4">
            <div className="mt-1 h-2.5 w-2.5 rounded-full bg-blue-500" />

            <div>
                <p className="text-sm font-medium text-slate-800">
                    {action}
                </p>
            </div>
        </div>
    )
}

export default ActionCard