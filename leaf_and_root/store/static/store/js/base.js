document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("searchToggle");
    const searchForm = document.getElementById("searchForm");

    if (toggleBtn && searchForm) {
        toggleBtn.addEventListener("click", () => {
            searchForm.classList.toggle("d-none");
        });
    }
    
    // Global toast helper
    const toastEl = document.getElementById("globalToast");
    const toastBody = document.getElementById("globalToastBody");
    if (toastEl && toastBody) {
        window.showToast = (message, type = "success", delay = 2000) => {
            toastBody.textContent = message || "";
            // swap bg classes
            toastEl.classList.remove("text-bg-success", "text-bg-danger", "text-bg-primary", "text-bg-warning");
            const map = { success: "text-bg-success", danger: "text-bg-danger", warning: "text-bg-warning", info: "text-bg-primary" };
            toastEl.classList.add(map[type] || "text-bg-success");
            // update delay if provided
            if (delay && toastEl.dataset) {
                toastEl.dataset.bsDelay = String(delay);
            }
            const toast = bootstrap.Toast.getOrCreateInstance(toastEl);
            toast.show();
        };
    }
});