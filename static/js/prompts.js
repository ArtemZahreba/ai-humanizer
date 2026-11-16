
document.addEventListener("DOMContentLoaded", () => {
    const promptsList = document.getElementById("prompts-list");
    const filters = document.querySelectorAll(".prompt-filter");

    if (!promptsList) return;

    let prompts = [];
    let currentFilter = "all";

    // Load prompts from API
    async function loadPrompts() {
        promptsList.textContent = "Loading prompts...";

        try {
            const clientId = getClientId();

            const response = await fetch(
                `/api/prompts?client_id=${encodeURIComponent(clientId)}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const data = await response.json();

            if (data.status !== "success") {
                throw new Error(data.message || "Failed to load prompts");
            }

            prompts = data.prompts || [];

            renderPrompts();

        } catch (error) {
            console.error("Prompts loading error:", error);

            promptsList.textContent =
                "Unable to load prompts. Please try again.";
        }
    }

    // Delete custom prompt
    async function deletePrompt(prompt) {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${prompt.name}"?`
        );

        if (!confirmed) return;

        try {
            const response = await fetch(`/api/prompts/${prompt.id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    client_id: getClientId()
                })
            });

            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(data.message || "Failed to delete prompt.");
            }

            prompts = prompts.filter(item => item.id !== prompt.id);

            renderPrompts();

        } catch (error) {
            console.error("Delete prompt error:", error);
            alert(error.message || "Unable to delete prompt.");
        }
    }

    // Render prompts
    function renderPrompts() {
        promptsList.replaceChildren();

        const filteredPrompts = prompts.filter(prompt => {
            if (currentFilter === "standard") {
                return prompt.is_default === true;
            }

            if (currentFilter === "custom") {
                return prompt.is_default === false;
            }

            return true;
        });

        if (filteredPrompts.length === 0) {
            const message = document.createElement("div");
            message.className = "history-message";
            message.textContent = "No prompts found.";

            promptsList.appendChild(message);
            return;
        }

        filteredPrompts.forEach(prompt => {
            const card = document.createElement("article");
            card.className = "prompt-card";

            const content = document.createElement("div");
            content.className = "prompt-card-content";

            const titleWrapper = document.createElement("div");
            titleWrapper.className = "prompt-card-title";

            const title = document.createElement("h3");
            title.textContent = prompt.name;

            const badge = document.createElement("span");
            badge.className = "prompt-badge";
            badge.textContent = prompt.is_default ? "Standard" : "My Prompt";

            titleWrapper.append(title, badge);

            const description = document.createElement("p");
            description.className = "prompt-card-description";
            description.textContent =
                prompt.description || "No description provided.";

            content.append(titleWrapper, description);

           const actions = document.createElement("div");
            actions.className = "prompt-card-actions";

            // View button
            const viewButton = document.createElement("button");
            viewButton.type = "button";
            viewButton.className = "prompt-action-button";
            viewButton.textContent = "View";

            viewButton.addEventListener("click", () => {
                openPromptModal("view", prompt);
            });

            actions.appendChild(viewButton);

            // Edit and Delete buttons for custom prompts
            if (!prompt.is_default) {
                const editButton = document.createElement("button");
                editButton.type = "button";
                editButton.className = "prompt-action-button";
                editButton.textContent = "Edit";

                editButton.addEventListener("click", () => {
                    openPromptModal("edit", prompt);
                });

                const deleteButton = document.createElement("button");
                deleteButton.type = "button";
                deleteButton.className =
                    "prompt-action-button prompt-delete-button";
                deleteButton.textContent = "Delete";

                deleteButton.addEventListener("click", () => {
                    deletePrompt(prompt);
                });

                actions.append(editButton, deleteButton);
            }

            card.append(content, actions);
            promptsList.appendChild(card);
        });
    }

    // Filter buttons
    filters.forEach(button => {
        button.addEventListener("click", () => {
            currentFilter = button.dataset.filter;

            filters.forEach(filter => {
                filter.classList.remove("active");
            });

            button.classList.add("active");

            renderPrompts();
        });
    });

    loadPrompts();


    // Prompt Modal
    const createButton = document.getElementById("create-prompt");
    const modal = document.getElementById("prompt-modal");
    const closeButton = document.getElementById("close-prompt-modal");
    const cancelButton = document.getElementById("cancel-prompt");
    const promptForm = document.getElementById("prompt-form");

    const promptName = document.getElementById("prompt-name");
    const promptContent = document.getElementById("prompt-content");
    const promptError = document.getElementById("prompt-error");
    const saveButton = document.getElementById("save-prompt");

    const modalTitle = document.getElementById("prompt-modal-title");
    const modalDescription = document.getElementById("prompt-modal-description");

    let modalMode = "create";
    let editingPromptId = null;

    // Open modal
    function openPromptModal(mode = "create", prompt = null) {
        modalMode = mode;
        editingPromptId = prompt ? prompt.id : null;

        promptError.hidden = true;
        promptError.textContent = "";

        promptForm.reset();

        promptName.value = prompt ? prompt.name : "";
        promptContent.value = prompt ? prompt.content : "";

        const isViewMode = mode === "view";

        promptName.readOnly = isViewMode;
        promptContent.readOnly = isViewMode;

        saveButton.hidden = isViewMode;
        saveButton.textContent = mode === "edit"
            ? "Save Changes"
            : "Save Prompt";

        if (mode === "view") {
            modalTitle.textContent = "View Prompt";
            modalDescription.textContent =
                "This prompt is available for viewing only.";
            cancelButton.textContent = "Close";
        } else if (mode === "edit") {
            modalTitle.textContent = "Edit Prompt";
            modalDescription.textContent =
                "Update your humanization style.";
            cancelButton.textContent = "Cancel";
        } else {
            modalTitle.textContent = "Create Prompt";
            modalDescription.textContent =
                "Create your own humanization style.";
            cancelButton.textContent = "Cancel";
        }

        modal.hidden = false;

        if (!isViewMode) {
            promptName.focus();
        }
    }

    // Close modal
    function closePromptModal() {
        modal.hidden = true;
        promptForm.reset();

        promptName.readOnly = false;
        promptContent.readOnly = false;

        modalMode = "create";
        editingPromptId = null;

        promptError.hidden = true;
        promptError.textContent = "";

        saveButton.hidden = false;
        saveButton.textContent = "Save Prompt";
    }

    // Modal event listeners
    createButton.addEventListener("click", () => {
        openPromptModal("create");
    });

    closeButton.addEventListener("click", closePromptModal);
    cancelButton.addEventListener("click", closePromptModal);

    modal.addEventListener("click", event => {
        if (event.target === modal) {
            closePromptModal();
        }
    });

    // Create or update prompt
    promptForm.addEventListener("submit", async event => {
        event.preventDefault();

        if (modalMode === "view") return;

        const name = promptName.value.trim();
        const content = promptContent.value.trim();

        promptError.hidden = true;

        if (!name || !content) {
            promptError.textContent = "Please fill in all required fields.";
            promptError.hidden = false;
            return;
        }

        saveButton.disabled = true;
        saveButton.textContent = "Saving...";

        try {
            const isEditing = modalMode === "edit";

            const url = isEditing
                ? `/api/prompts/${editingPromptId}`
                : "/api/prompts";

            const response = await fetch(url, {
                method: isEditing ? "PUT" : "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    client_id: getClientId(),
                    name,
                    content,
                    ...(isEditing ? {} : { category: "general" })
                })
            });

            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(
                    data.message || "Failed to save prompt."
                );
            }

            if (isEditing) {
                const updatedPrompt = data.prompt || {
                    ...prompts.find(p => p.id === editingPromptId),
                    name,
                    content
                };

                prompts = prompts.map(prompt =>
                    prompt.id === editingPromptId
                        ? updatedPrompt
                        : prompt
                );
            } else {
                prompts.push(data.prompt);
            }

            currentFilter = "all";

            filters.forEach(filter => {
                filter.classList.toggle(
                    "active",
                    filter.dataset.filter === "all"
                );
            });

            renderPrompts();
            closePromptModal();

        } catch (error) {
            console.error("Save prompt error:", error);

            promptError.textContent =
                error.message || "Something went wrong.";

            promptError.hidden = false;

        } finally {
            saveButton.disabled = false;
            saveButton.textContent = modalMode === "edit"
                ? "Save Changes"
                : "Save Prompt";
        }
    });

    loadPrompts();

});

    