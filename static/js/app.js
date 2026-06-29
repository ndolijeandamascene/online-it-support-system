(function () {
    const root = document.documentElement;
    const savedTheme = localStorage.getItem("support-theme");
    if (savedTheme) {
        root.setAttribute("data-bs-theme", savedTheme);
    }

    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("show"));
    }

    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const nextTheme = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
            root.setAttribute("data-bs-theme", nextTheme);
            localStorage.setItem("support-theme", nextTheme);
        });
    }

    const loadingBar = document.getElementById("loadingBar");
    if (loadingBar) {
        loadingBar.classList.add("active");
        window.addEventListener("load", () => {
            loadingBar.classList.add("done");
            setTimeout(() => loadingBar.classList.remove("active", "done"), 500);
        });
    }

    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!window.confirm(form.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll(".toast").forEach((toastNode) => {
        if (window.bootstrap) {
            new bootstrap.Toast(toastNode, { delay: 3500 }).show();
        }
    });

    function jsonFromScript(id) {
        const node = document.getElementById(id);
        return node ? JSON.parse(node.textContent) : [];
    }

    function chartColors() {
        return ["#176b87", "#f4a261", "#2a9d8f", "#e76f51", "#6c757d", "#8e7cc3"];
    }

    window.SupportCharts = {
        renderDoughnut(canvasId, labelsId, valuesId) {
            const canvas = document.getElementById(canvasId);
            if (!canvas || !window.Chart) return;
            new Chart(canvas, {
                type: "doughnut",
                data: {
                    labels: jsonFromScript(labelsId),
                    datasets: [{ data: jsonFromScript(valuesId), backgroundColor: chartColors(), borderWidth: 0 }],
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: "bottom" } },
                },
            });
        },
        renderBar(canvasId, labelsId, valuesId) {
            const canvas = document.getElementById(canvasId);
            if (!canvas || !window.Chart) return;
            new Chart(canvas, {
                type: "bar",
                data: {
                    labels: jsonFromScript(labelsId),
                    datasets: [{ data: jsonFromScript(valuesId), backgroundColor: "#176b87", borderRadius: 6 }],
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
                },
            });
        },
    };
})();
