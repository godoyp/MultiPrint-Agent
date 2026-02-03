let SESSION_TOKEN = null;

export function getSessionToken() {
    return SESSION_TOKEN;
}

export function isAuthenticated() {
    return !!SESSION_TOKEN;
}

export async function handshake() {
    const res = await fetch("/auth/handshake", {
        method: "POST"
    });

    if (!res.ok) {
        throw new Error("Unable to authenticate with agent");
    }

    const data = await res.json();
    SESSION_TOKEN = data.token;
}
