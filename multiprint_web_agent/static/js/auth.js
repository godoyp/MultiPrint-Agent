let SESSION_TOKEN = 'teste de token';

export function getSessionToken() {
    return SESSION_TOKEN;
}

export function isAuthenticated() {
    return !!SESSION_TOKEN;
}

export async function handshake() {
    const res = await fetch("/api/v1/auth/handshake", {
        method: "POST"
    });

    if (!res.ok) {
        throw new Error("Unable to authenticate with agent");
    }

    const response = await res.json();
    SESSION_TOKEN = response.data.token;
}
