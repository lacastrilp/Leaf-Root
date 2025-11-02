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
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Update the heart icon
                        const icon = this.querySelector(".wishlist-icon");
                        if (data.in_wishlist) {
                            icon.classList.remove("bi-heart");
                            icon.classList.add("bi-heart-fill", "active");
                        } else {
                            icon.classList.remove("bi-heart-fill", "active");
                            icon.classList.add("bi-heart");
                        }
                        // Show toast
                        const message = data.message || (data.in_wishlist ? "Added to wishlist" : "Removed from wishlist");
                        if (window.showToast) {
                            window.showToast(message, data.in_wishlist ? "success" : "danger");
                        }
                    }
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
                .then(res => res.json())
                .then(data => {
                    // Show toast on success
                    if (window.showToast) {
                        window.showToast("Added to cart", "success");
                    }
                    // Optionally reload modal to update stock/cart count
                    const productId = this.dataset.productId;
                    if (productId) {
                        const url = `/catalog/product/${productId}/`;
                        openProductModal(url);
                    }
                })
                .catch(err => console.error(err));
            });
        });
    }
});
