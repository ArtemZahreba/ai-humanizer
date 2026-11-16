
function getClientId() {
    let clientId = localStorage.getItem("ai_humanizer_client_id");

    if (!clientId) {
        clientId = crypto.randomUUID();
        localStorage.setItem("ai_humanizer_client_id", clientId);
    }

    return clientId;
}
