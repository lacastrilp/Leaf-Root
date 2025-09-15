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
        .catch(err => console.error("Wishlist error:", err));
    });
});
