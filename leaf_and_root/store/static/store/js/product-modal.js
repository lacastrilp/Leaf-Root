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
        // Initialize star rating if present in modal content
        if (window.initStarRating) {
            window.initStarRating();
        }
        // Review submit via AJAX (stay in modal)
        const reviewForm = document.querySelector("#productModal #reviewForm");
        if (reviewForm) {
            reviewForm.addEventListener("submit", function (e) {
                e.preventDefault();
                fetch(this.action, {
                    method: "POST",
                    body: new FormData(this),
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                .then(res => res.json().catch(() => null))
                .then(data => {
                    if (data && data.success) {
                        if (window.showToast) {
                            window.showToast(data.message || "Review submitted", "success");
                        }
                        const productId = this.dataset.productId;
                        if (productId) {
                            const url = `/catalog/product/${productId}/`;
                            openProductModal(url);
                        }
                    } else {
                        // Try to extract error messages
                        if (window.showToast) {
                            const msg = (data && data.message) || "There was a problem submitting your review";
                            window.showToast(msg, "danger");
                        }
                    }
                })
                .catch(err => {
                    console.error(err);
                    if (window.showToast) {
                        window.showToast("Network error submitting review", "danger");
                    }
                });
            });
        }
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
                    if (data.success) {
                        // Call the same renderSidebar function from cart.js to open sidebar
                        if (window.renderCartSidebar) {
                            window.renderCartSidebar(data);
                        }
                        // Show toast
                        if (window.showToast) {
                            window.showToast("Added to cart", "success");
                        }
                        // Reload modal to update stock
                        const productId = this.dataset.productId;
                        if (productId) {
                            const url = `/catalog/product/${productId}/`;
                            openProductModal(url);
                        }
                    }
                })
                .catch(err => console.error(err));
            });
        });

        // Delete review AJAX
        document.querySelectorAll("#productModal .delete-review-form").forEach(form => {
            form.addEventListener("submit", function (e) {
                e.preventDefault();
                
                const reviewId = this.dataset.reviewId;
                const formData = new FormData(this);
                
                fetch(this.action, {
                    method: "POST",
                    body: formData,
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Eliminar la review del DOM
                        this.closest(".mb-3").remove();
                        
                        // Actualizar contador y promedio
                        const ratingElement = document.querySelector("#productModal .fw-semibold");
                        if (ratingElement) {
                            if (data.review_count > 0) {
                                ratingElement.textContent = data.avg_rating + "/5";
                                const countElement = ratingElement.nextElementSibling;
                                if (countElement) {
                                    countElement.textContent = `(${data.review_count})`;
                                }
                            } else {
                                ratingElement.parentElement.innerHTML = '<small class="text-muted">No ratings yet</small>';
                            }
                        }
                        
                        if (window.showToast) {
                            window.showToast("Review deleted", "success");
                        }
                    }
                })
                .catch(error => console.error("Error:", error));
            });
        });
    }
});
