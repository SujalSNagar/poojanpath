document.querySelectorAll(".add-to-cart-form").forEach((form) => {
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const data = await response.json();

      if (data.success) {
        document.querySelectorAll(".cart-count").forEach((item) => {
          item.textContent = data.cart_count;
        });

        const toastElement = document.getElementById("cartToast");

      if (toastElement) {
        const toast = new bootstrap.Toast(toastElement, {
          delay: 3000,
        });
      
        toast.show();
      }
      } else {
        alert(data.message);
      }
    } catch (error) {
      alert("Something went wrong. Please try again.");
    }
  });
});


