document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".add-to-cart-form");

    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // evita que cargue JSON en la página

            fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })
            .then(response => response.json())
            .then(data => {
                // aquí llamas tu función de abrir sidebar
                abrirSidebarCarrito(data);
            })
            .catch(error => console.error("Error:", error));
        });
    });
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
