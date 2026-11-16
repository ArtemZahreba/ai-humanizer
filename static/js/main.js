
document.addEventListener("DOMContentLoaded", () => {
    const inputText = document.getElementById("input-text");
    const charCounter = document.getElementById("char-counter");

    // Navigation
    const navItems = document.querySelectorAll(".nav-item");
    const views = document.querySelectorAll(".view");

    const pageTitles = {
        humanization: {
            title: "Text Humanization",
            description: "Rewrite AI-generated text to sound natural, human, and unique."
        },
        prompts: {
            title: "Prompts",
            description: "Create and manage your humanization styles."
        },
        history: {
            title: "History",
            description: "Your previous humanizations."
        }
    };

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const target = item.dataset.view;

            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");

            views.forEach(view => view.classList.remove("active"));

            document
                .getElementById(`view-${target}`)
                .classList.add("active");

            document.getElementById("page-title").textContent =
                pageTitles[target].title;

            document.getElementById("page-description").textContent =
                pageTitles[target].description;
        });
    });

    // Theme
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");

    function updateThemeIcon(theme) {
        themeIcon.textContent = theme === "dark" ? "☀" : "☾";
    }

    function setTheme(theme) {
        document.documentElement.dataset.theme = theme;

        localStorage.setItem("ai-humanizer-theme", theme);

        updateThemeIcon(theme);
    }

    // Initialize theme
    const savedTheme = localStorage.getItem("ai-humanizer-theme");
    const initialTheme = savedTheme === "dark" ? "dark" : "light";

    setTheme(initialTheme);

    // Toggle theme
    themeToggle.addEventListener("click", () => {
        const currentTheme = document.documentElement.dataset.theme;
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        setTheme(newTheme);
    });
    
    // Clear input
    document.getElementById("clear-input").addEventListener("click", () => {
        inputText.value = "";
        charCounter.textContent = "0 / 5000 characters";
        inputText.focus();
    });

    // Copy output
    document.getElementById("copy-output").addEventListener("click", async () => {
        const output = document.getElementById("output-text");
        const text = output.innerText.trim();

        if (!text) return;

        try {
            await navigator.clipboard.writeText(text);
            alert("Text copied!");
        } catch (error) {
            alert("Unable to copy text.");
        }
    });

    // Humanization placeholder
    // document.getElementById("humanize-button").addEventListener("click", () => {
    //     if (!inputText.value.trim()) {
    //         alert("Please enter some text first.");
    //         return;
    //     }

    //     alert("AI integration will be implemented in the next stage.");
    // });

});
