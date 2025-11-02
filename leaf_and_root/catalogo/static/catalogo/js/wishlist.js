document.addEventListener("DOMContentLoaded", () => {
  // Manejo de formulario único con mensaje
  const wishlistForm = document.getElementById("wishlistForm");
  const wishlistMessage = document.getElementById("wishlistMessage");

  if (wishlistForm && wishlistMessage) {
    wishlistForm.addEventListener("submit", (e) => {
      e.preventDefault();
      fetch(wishlistForm.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": wishlistForm.querySelector("[name=csrfmiddlewaretoken]").value,
          "X-Requested-With": "XMLHttpRequest",
        },
        body: new FormData(wishlistForm),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const message = data.message || (data.in_wishlist ? "Added to wishlist" : "Removed from wishlist");
            if (window.showToast) {
              window.showToast(message, data.in_wishlist ? "success" : "danger");
            } else {
              wishlistMessage.textContent = message;
              wishlistMessage.classList.remove("d-none");
              wishlistMessage.classList.add("show");
              setTimeout(() => wishlistMessage.classList.add("d-none"), 3000);
            }
          }
        })
        .catch((err) => console.error("Wishlist error:", err));
    });
  }

  // Manejo de múltiples formularios (listado de productos)
  document.querySelectorAll(".wishlist-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      fetch(form.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
          "X-Requested-With": "XMLHttpRequest",
        },
        body: new FormData(form),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const icon = form.querySelector(".wishlist-icon");
            if (data.in_wishlist) {
              icon.classList.remove("bi-heart");
              icon.classList.add("bi-heart-fill", "active");
            } else {
              icon.classList.remove("bi-heart-fill", "active");
              icon.classList.add("bi-heart");
            }
            const message = data.message || (data.in_wishlist ? "Added to wishlist" : "Removed from wishlist");
            if (window.showToast) {
              window.showToast(message, data.in_wishlist ? "success" : "danger");
            }
          }
        })
        .catch((err) => console.error("Wishlist error:", err));
    });
  });
});
