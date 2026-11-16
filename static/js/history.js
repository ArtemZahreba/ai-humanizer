
document.addEventListener("DOMContentLoaded", () => {
    const historyList = document.getElementById("history-list");
    const searchInput = document.getElementById("history-search");

    if (!historyList || !searchInput) return;

    let historyRecords = [];

    async function loadHistory() {
        historyList.textContent = "Loading history...";

        try {
            const clientId = getClientId();

            const response = await fetch(
                `/api/history?client_id=${encodeURIComponent(clientId)}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const data = await response.json();

            if (data.status !== "success") {
                throw new Error(data.message || "Failed to load history");
            }

            historyRecords = data.history || [];

            renderHistory(historyRecords);

        } catch (error) {
            console.error("History loading error:", error);

            historyList.textContent =
                "Unable to load history. Please try again.";
        }
    }

    function renderHistory(records) {
        historyList.replaceChildren();

        if (records.length === 0) {
            const message = document.createElement("div");
            message.className = "history-message";
            message.textContent = "No humanizations found.";

            historyList.appendChild(message);
            return;
        }

        records.forEach(record => {
            const card = document.createElement("article");
            card.className = "history-item";

            const header = document.createElement("div");
            header.className = "history-item-header";

            const model = document.createElement("span");
            model.className = "history-item-model";
            model.textContent = record.model_id;

            const date = document.createElement("span");
            date.className = "history-item-date";
            date.textContent = record.created_at
                ? new Date(record.created_at).toLocaleString()
                : "Unknown date";

            header.append(model, date);

            const preview = document.createElement("p");
            preview.className = "history-item-preview";
            preview.textContent = record.original_text;

            card.append(header, preview);
            historyList.appendChild(card);
        });
    }

    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim().toLowerCase();

        const filteredRecords = historyRecords.filter(record =>
            record.original_text.toLowerCase().includes(query) ||
            record.result_text.toLowerCase().includes(query)
        );

        renderHistory(filteredRecords);
    });

    loadHistory();
});
