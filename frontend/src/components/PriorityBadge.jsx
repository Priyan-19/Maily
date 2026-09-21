function PriorityBadge({ importance }) {
    const styles = {
        high: "bg-red-100 text-red-700",
        medium: "bg-yellow-100 text-yellow-700",
        low: "bg-green-100 text-green-700",
    }

    return (
        <span
            className={`rounded-full px-3 py-1 text-xs font-semibold ${styles[importance] || "bg-gray-100 text-gray-700"
                }`}
        >
            {importance || "unknown"}
        </span>
    )
}

export default PriorityBadge