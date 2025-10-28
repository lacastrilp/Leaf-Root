document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("searchToggle");
    const searchForm = document.getElementById("searchForm");

    if (toggleBtn && searchForm) {
        toggleBtn.addEventListener("click", () => {
            searchForm.classList.toggle("d-none");
        });
    }
});