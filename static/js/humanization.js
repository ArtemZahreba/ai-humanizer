
document.addEventListener("DOMContentLoaded", () => {
    const modelSelect = document.getElementById("model-select");
    const promptSelect = document.getElementById("prompt-select");
    const inputText = document.getElementById("input-text");
    const outputText = document.getElementById("output-text");
    const humanizeButton = document.getElementById("humanize-button");

    if (!modelSelect || !promptSelect || !inputText || !outputText || !humanizeButton) {
        return;
    }

    // Load available AI models
    async function loadModels() {
        modelSelect.disabled = true;
        modelSelect.replaceChildren(new Option("Loading models...", ""));

        try {
            const response = await fetch("/api/models");
            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(data.message || "Failed to load models");
            }

            const models = data.models || [];
            modelSelect.replaceChildren();

            if (models.length === 0) {
                modelSelect.add(new Option("No models available", ""));
                return;
            }

            models.forEach(model => {
                modelSelect.add(new Option(model.name, String(model.id)));
            });

            modelSelect.value = String(models[0].id);

        } catch (error) {
            console.error("Models loading error:", error);
            modelSelect.replaceChildren(
                new Option("Unable to load models", "")
            );
        } finally {
            modelSelect.disabled = !modelSelect.value;
        }
    }

    // Load available prompts
    async function loadPrompts() {
        promptSelect.disabled = true;
        promptSelect.replaceChildren(new Option("Loading prompts...", ""));

        try {
            const clientId = getClientId();

            const response = await fetch(
                `/api/prompts?client_id=${encodeURIComponent(clientId)}`
            );

            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(data.message || "Failed to load prompts");
            }

            const prompts = data.prompts || [];
            promptSelect.replaceChildren();

            if (prompts.length === 0) {
                promptSelect.add(new Option("No prompts available", ""));
                return;
            }

            prompts.forEach(prompt => {
                const label = prompt.is_default
                    ? `${prompt.name} (Standard)`
                    : `${prompt.name} (Custom)`;

                promptSelect.add(new Option(label, String(prompt.id)));
            });

            promptSelect.value = String(prompts[0].id);

        } catch (error) {
            console.error("Prompts loading error:", error);
            promptSelect.replaceChildren(
                new Option("Unable to load prompts", "")
            );
        } finally {
            promptSelect.disabled = !promptSelect.value;
        }
    }

    // Send text for humanization
    async function humanizeText() {
        const text = inputText.value.trim();

        if (!text) {
            alert("Please enter text to humanize.");
            inputText.focus();
            return;
        }

        const modelId = Number(modelSelect.value);
        const promptId = Number(promptSelect.value);

        if (!modelId || !promptId) {
            alert("Please select an AI model and a prompt.");
            return;
        }

        humanizeButton.disabled = true;
        humanizeButton.textContent = "Processing...";

        outputText.textContent = "Humanizing your text. Please wait...";

        try {
            const response = await fetch("/api/humanize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    client_id: getClientId(),
                    text: text,
                    model_id: modelId,
                    prompt_id: promptId
                })
            });

            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(data.message || "Humanization failed");
            }

            const result = data.result;

            outputText.textContent = result.result_text;

            console.log("Humanization completed:", result);

        } catch (error) {
            console.error("Humanization error:", error);
            outputText.textContent = `Error: ${error.message}`;

        } finally {
            humanizeButton.disabled = false;
            humanizeButton.textContent = "✧ Humanize Text";
        }
    }

    humanizeButton.addEventListener("click", humanizeText);

    // Initialize selectors
    loadModels();
    loadPrompts();
});
