document.addEventListener("DOMContentLoaded", function() {
    const sesization = document.getElementById("status");
    const id = document.getElementById("sesization_id");

    sesization.addEventListener("click", function() { 
        console.log("Sesizare trimisa");
            const csrfToken = document.getElementById("csrf-token").value;

            fetch(`/change_status/${id.value}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // ✅ Add CSRF token
                },
                body: JSON.stringify({ 
                    status: "Luat la cunostiinta"
                })
            })


            sesization.disabled = true;
    });
});
