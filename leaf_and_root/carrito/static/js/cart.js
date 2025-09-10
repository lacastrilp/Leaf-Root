document.addEventListener("DOMContentLoaded", () => {
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
                        <form method="post" action="/cart/remove/${item.id}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie("csrftoken")}">
                            <button type="submit" class="btn btn-danger btn-sm">✖</button>
                        </form>
                    `;
                    list.appendChild(li);
                });

                cartContent.appendChild(list);

                // Total
                cartContent.innerHTML += `
                    <div class="d-flex justify-content-between">
                        <strong>Total:</strong> <span>$${data.total_price}</span>
                    </div>
                    <a href="/cart/" class="btn btn-primary w-100 mt-3">Ver Carrito</a>
                `;

                // Mostrar sidebar
                const sidebar = new bootstrap.Offcanvas(document.getElementById("cartSidebar"));
                sidebar.show();

                // Bind eventos para selects
                bindUpdateForms();
            }
        });
    });

    // Función para manejar cambios de cantidad
    function bindUpdateForms() {
        document.querySelectorAll(".update-form select").forEach(select => {
            select.addEventListener("change", async (e) => {
                e.preventDefault();
                const form = select.closest("form");
                const formData = new FormData(form);

                await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {"X-Requested-With": "XMLHttpRequest"}
                });

                // Opcional: refrescar sidebar automáticamente
                document.querySelector(".add-to-cart-form button").click();
            });
        });
    }

    // Helper para CSRF
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



function abrirSidebarCarrito(data) {
    const sidebar = document.getElementById("cartSidebar");
    sidebar.classList.add("active");  
    // Aquí puedes actualizar el contenido del sidebar con data
    const cartItemsContainer = document.getElementById("cartItems");
    const cartTotal = document.getElementById("cartTotal");

    cartItemsContainer.innerHTML = "";
    data.cart_items.forEach(item => {
        cartItemsContainer.innerHTML += `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}" style="width:50px; height:50px; object-fit:cover; margin-right:10px;">
                <span>${item.name}</span> x${item.quantity} - $${item.subtotal.toFixed(2)}
            </div>
        `;
    });
    cartTotal.textContent = `$${data.total_price.toFixed(2)}`;
    cartItemsContainer.parentElement.classList.add("active");
    
}
