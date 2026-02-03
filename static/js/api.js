import { getSessionToken } from "./auth.js";

function authHeaders(extra = {}) {
    const token = getSessionToken();
    return token
        ? { ...extra, "Authorization": `Bearer ${token}` }
        : extra;
}

export async function apiGet(url) {
    const res = await fetch(url, {
        headers: authHeaders()
    });

    if (res.status === 429) {
        throw new Error("RATE_LIMIT");
    }

    if (!res.ok) throw new Error("GET failed");
    return res.json();
}

export async function apiPost(url, body = null) {
    const res = await fetch(url, {
        method: "POST",
        headers: authHeaders(
            body ? { "Content-Type": "application/json" } : {}
        ),
        body: body ? JSON.stringify(body) : null
    });

    if (res.status === 429) {
        throw new Error("RATE_LIMIT");
    }

    if (!res.ok) throw new Error("POST failed");
    return res;
}

export async function apiPut(url, data) {
    const res = await fetch(url, {
        method: "PUT",
        headers: authHeaders({
            "Content-Type": "application/json"
        }),
        body: JSON.stringify(data)
    });

    if (res.status === 429) {
        throw new Error("RATE_LIMIT");
    }

    if (!res.ok) throw new Error("API PUT failed");
    return res.json();
}
