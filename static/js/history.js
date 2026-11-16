
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

            renderFilteredHistory();

        } catch (error) {
            console.error("History loading error:", error);

            historyList.textContent =
                "Unable to load history. Please try again.";
        }
    }

    function renderFilteredHistory() {
        const query = searchInput.value.trim().toLowerCase();

        const filteredRecords = historyRecords.filter(record =>
            record.original_text.toLowerCase().includes(query) ||
            record.result_text.toLowerCase().includes(query)
        );

        renderHistory(filteredRecords);
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

            // Prompt name
            const prompt = document.createElement("span");
            prompt.className = "history-item-prompt";
            prompt.textContent = record.prompt_name || "Unknown prompt";

            const date = document.createElement("span");
            date.className = "history-item-date";
            date.textContent = record.created_at
                ? new Date(record.created_at).toLocaleString()
                : "Unknown date";

            const meta = document.createElement("div");
            meta.className = "history-item-meta";

            meta.append(model, prompt);
            header.append(meta, date);

            const content = document.createElement("div");
            content.className = "history-item-content";

            // Original text
            const originalBlock = document.createElement("div");
            originalBlock.className = "history-text-block";

            const originalTitle = document.createElement("h4");
            originalTitle.textContent = "Original text";

            const originalText = document.createElement("p");
            originalText.className = "history-item-preview";
            originalText.textContent = record.original_text;

            originalBlock.append(originalTitle, originalText);

            // Humanized text
            const resultBlock = document.createElement("div");
            resultBlock.className = "history-text-block";

            const resultTitle = document.createElement("h4");
            resultTitle.textContent = "Humanized text";

            const resultText = document.createElement("p");
            resultText.className = "history-item-preview";
            resultText.textContent = record.result_text;

            resultBlock.append(resultTitle, resultText);

            content.append(originalBlock, resultBlock);
            card.append(header, content);
            historyList.appendChild(card);
        });
    }

    searchInput.addEventListener("input", renderFilteredHistory);
    // Refresh history whenever the History tab is opened
    document
        .querySelectorAll('.nav-item[data-view="history"]')
        .forEach(item => {
            item.addEventListener("click", loadHistory);
    });
    loadHistory();
});
