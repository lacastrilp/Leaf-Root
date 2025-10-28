document.addEventListener("DOMContentLoaded", () => {
    const wishlistForm = document.getElementById("wishlistForm");
    const wishlistMessage = document.getElementById("wishlistMessage");

    if (!wishlistForm) return;

    wishlistForm.addEventListener("submit", (e) => {
        e.preventDefault(); // <- Esto evita que recargue la página

        fetch(wishlistForm.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": wishlistForm.querySelector("[name=csrfmiddlewaretoken]").value,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: new FormData(wishlistForm)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                wishlistMessage.textContent = data.message;
                wishlistMessage.classList.remove("d-none");
                wishlistMessage.classList.add("show");

                setTimeout(() => {
                    wishlistMessage.classList.add("d-none");
                }, 3000);
            }
        })
        .catch(err => console.error("Wishlist error:", err));document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll(".wishlist-form");

    forms.forEach(form => {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            fetch(form.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: new FormData(form)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const icon = form.querySelector(".wishlist-icon");
                    if (data.in_wishlist) {
                        icon.classList.remove("bi-heart");
                        icon.classList.add("bi-heart-fill", "text-danger");
                    } else {
                        icon.classList.remove("bi-heart-fill", "text-danger");
                        icon.classList.add("bi-heart");
                    }
                }
            })
            .catch(err => console.error("Wishlist error:", err));
        });
    });
});

    });
});
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', () => {
            const form = button.closest('form');
            const productId = form.dataset.productId;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            const icon = button.querySelector('.wishlist-icon');

            fetch(`/toggle_wishlist/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // alternar clase filled según respuesta
                    if (data.in_wishlist) {
                        icon.classList.add('filled');
                    } else {
                        icon.classList.remove('filled');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});