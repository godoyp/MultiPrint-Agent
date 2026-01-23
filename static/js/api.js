export async function apiGet(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error("GET failed");
    return res.json();
}

export async function apiPost(url, body = null) {
    const res = await fetch(url, {
        method: "POST",
        headers: body ? { "Content-Type": "application/json" } : {},
        body: body ? JSON.stringify(body) : null
    });

    if (!res.ok) throw new Error("POST failed");
    return res;
}
