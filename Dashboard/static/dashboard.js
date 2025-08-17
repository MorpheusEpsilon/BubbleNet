document.addEventListener("DOMContentLoaded", () => {
    const addForms = document.querySelectorAll(".add-form");
    const removeForms = document.querySelectorAll(".remove-form");

    addForms.forEach(form => {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });
            if (response.ok) {
                location.reload(); // reload to update tables
            }
        });
    });

    removeForms.forEach(form => {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });
            if (response.ok) {
                location.reload();
            }
        });
    });
});
