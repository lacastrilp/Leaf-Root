document.addEventListener("DOMContentLoaded", function () {
    // Detectar clics en enlaces de productos (imagen o título)
    document.querySelectorAll(".product-link").forEach(function (element) {
        element.addEventListener("click", function (e) {
            e.preventDefault();

            const url = this.getAttribute("href");

            // Petición AJAX para traer el contenido del detalle
            fetch(url, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Error al cargar detalle");
                    }
                    return response.text();
                })
                .then(html => {
                    // Inyectar contenido en el modal
                    const modalBody = document.querySelector("#productModal .modal-body");
                    modalBody.innerHTML = html;

                    // Mostrar modal
                    const modal = new bootstrap.Modal(document.getElementById("productModal"));
                    modal.show();
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        });
    });
});
