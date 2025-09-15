document.addEventListener("DOMContentLoaded", function () {
    // --- CLICK EN PRODUCTO (abre modal) ---
    document.querySelectorAll(".product-link").forEach(function (element) {
        element.addEventListener("click", function (e) {
            e.preventDefault();
            openProductModal(this.getAttribute("href"));
        });
    });

    // --- FUNCIÓN REUTILIZABLE PARA CARGAR MODAL ---
    function openProductModal(url) {
        fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.text())
        .then(html => {
            const modalBody = document.querySelector("#productModal .modal-body");
            modalBody.innerHTML = html;

            // Re-enganchar listeners dentro del modal
            attachModalListeners();

            const modal = new bootstrap.Modal(document.getElementById("productModal"));
            modal.show();
        })
        .catch(error => console.error("Error:", error));
    }

    // --- INTERCEPTAR FORMULARIOS EN EL MODAL ---
    function attachModalListeners() {
        // Wishlist AJAX
        document.querySelectorAll("#productModal .wishlist-form").forEach(form => {
            form.addEventListener("submit", function (e) {
                e.preventDefault();
                fetch(this.action, {
                    method: "POST",
                    body: new FormData(this),
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                .then(() => {
                    const url = window.location.origin + this.getAttribute("action")
                        .replace("toggle_wishlist", "product_detail");
                    openProductModal(url);
                })
                .catch(err => console.error(err));
            });
        });

        // Add to cart AJAX
        document.querySelectorAll("#productModal .cart-form").forEach(form => {
            form.addEventListener("submit", function (e) {
                e.preventDefault();
                fetch(this.action, {
                    method: "POST",
                    body: new FormData(this),
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                .then(() => {
                    const url = window.location.origin + this.getAttribute("action")
                        .split("?")[0]
                        .replace("add_to_cart", "product_detail");
                    openProductModal(url);
                })
                .catch(err => console.error(err));
            });
        });
    }
});
