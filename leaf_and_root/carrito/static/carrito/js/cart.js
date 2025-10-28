document.addEventListener("DOMContentLoaded", () => {
    // Bind para agregar al carrito
    document.querySelectorAll(".add-to-cart-form").forEach(form => {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const url = form.action;
            const formData = new FormData(form);

            const response = await fetch(url, {
                method: "POST",
                body: formData,
                headers: {"X-Requested-With": "XMLHttpRequest"}
            });

            const data = await response.json();
            if (data.success) {
                renderSidebar(data);
            }
        });
    });

    // Renderizar contenido del carrito en sidebar
    function renderSidebar(data) {
        const cartContent = document.getElementById("cartContent");
        cartContent.innerHTML = "";

        let list = document.createElement("ul");
        list.classList.add("list-group", "mb-3");

        data.cart_items.forEach(item => {
            const li = document.createElement("li");
            li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-start");

            li.innerHTML = `
                <div class="ms-2 me-auto">
                    <div class="fw-bold">${item.name}</div>
                    <form method="post" action="/cart/update/${item.id}/" class="update-form">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie("csrftoken")}">
                        <select name="quantity" class="form-select form-select-sm mt-2" style="width:80px;">
                            ${Array.from({length: 10}, (_, i) => i+1).map(num => `
                                <option value="${num}" ${num === item.quantity ? "selected" : ""}>${num}</option>
                            `).join("")}
                        </select>
                    </form>
                    <small class="text-muted">Precio: $${item.price}</small><br>
                    <small class="text-muted">Subtotal: $${item.subtotal}</small>
                </div>
                <form method="post" action="/cart/remove/${item.id}/" class="remove-form">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie("csrftoken")}">
                    <button type="submit" class="btn btn-danger btn-sm">✖</button>
                </form>
            `;
            list.appendChild(li);
        });

        cartContent.appendChild(list);

        cartContent.innerHTML += `
            <div class="d-flex justify-content-between">
                <strong>Total:</strong> <span>$${data.total_price}</span>
            </div>
            <a href="/cart/" class="btn btn-primary w-100 mt-3">Ver Carrito</a>
        `;

        // Mostrar sidebar
        const sidebarElement = document.getElementById("cartSidebar");
        let sidebar = bootstrap.Offcanvas.getInstance(sidebarElement);
        if (!sidebar) {
            sidebar = new bootstrap.Offcanvas(sidebarElement);
        }
        sidebar.show();

        // Bind dinámico para selects
        bindUpdateForms();
        bindRemoveForms();
    }

    // Manejar cambios de cantidad
    function bindUpdateForms() {
        document.querySelectorAll(".update-form select").forEach(select => {
            select.addEventListener("change", async (e) => {
                e.preventDefault();
                const form = select.closest("form");
                const formData = new FormData(form);

                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {"X-Requested-With": "XMLHttpRequest"}
                });
                const data = await response.json();
                if (data.success) {
                    renderSidebar(data);
                }
            });
        });
    }

    // Manejar eliminación
    function bindRemoveForms() {
        document.querySelectorAll(".remove-form").forEach(form => {
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const formData = new FormData(form);

                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {"X-Requested-With": "XMLHttpRequest"}
                });
                const data = await response.json();
                if (data.success) {
                    renderSidebar(data);
                }
            });
        });
    }

    // Helper CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// ACAAA

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("productModal");
    const modalContent = modal.querySelector(".modal-content");

    // Bind para abrir modal con AJAX
    document.querySelectorAll(".product-detail-link").forEach(link => {
        link.addEventListener("click", async (e) => {
            e.preventDefault();
            const response = await fetch(link.href, {headers: {"X-Requested-With": "XMLHttpRequest"}});
            const html = await response.text();
            modalContent.innerHTML = html;

            // Re-binds dentro del modal
            bindCartForms();
            bindReviewForms();
        });
    });

    // Binds reutilizables
    function bindCartForms() {
        modalContent.querySelectorAll(".add-to-cart-form").forEach(form => {
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const url = form.action;
                const formData = new FormData(form);
                const response = await fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {"X-Requested-With": "XMLHttpRequest"}
                });
                const data = await response.json();
                if (data.success) {
                    renderSidebar(data); // ya lo tienes definido
                }
            });
        });
    }

    function bindReviewForms() {
        modalContent.querySelectorAll(".review-form").forEach(form => {
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const url = form.action;
                const formData = new FormData(form);
                const response = await fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {"X-Requested-With": "XMLHttpRequest"}
                });
                const html = await response.text();
                modalContent.innerHTML = html; // recarga modal con reviews actualizados
                bindCartForms();
                bindReviewForms();
            });
        });
    }
});
