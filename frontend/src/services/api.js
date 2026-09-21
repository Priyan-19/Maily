import axios from "axios"

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
})

export const getEmails = async (limit = 50, offset = 0) => {
    const response = await api.get("/api/emails", {
        params: {
            limit,
            offset,
        },
    })

    return response.data
}

export const syncEmails = async () => {
    const response = await api.post("/api/emails/sync")

    return response.data
}

export const analyzeEmail = async (emailId) => {
    const response = await api.post(
        `/api/analysis/email/${emailId}`
    )

    return response.data
}

export const generateDigest = async () => {
    const response = await api.post("/api/digest/generate")

    return response.data
}

export const getTodayDigest = async () => {
    const response = await api.get("/api/digest/today")

    return response.data
}

export const getEmail = async (emailId) => {
    const response = await api.get(`/api/emails/${emailId}`)

    return response.data
}

export const getSettings = async () => {
    const response = await api.get("/api/settings")

    return response.data
}

export const updateSettings = async (data) => {
    const response = await api.put("/api/settings", data)

    return response.data
}

export const suggestReply = async (emailId, instructions = "") => {
    const response = await api.post(`/api/emails/${emailId}/suggest-reply`, null, {
        params: { instructions },
    })

    return response.data
}

export const createDraft = async (emailId, replyBody) => {
    const response = await api.post(`/api/emails/${emailId}/create-draft`, null, {
        params: { reply_body: replyBody },
    })

    return response.data
}

export const getBriefing = async () => {
    const response = await api.get("/api/digest/briefing")

    return response.data
}

export const clearAllEmails = async () => {
    const response = await api.delete("/api/emails/clear-all")

    return response.data
}

export default api