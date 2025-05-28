document.addEventListener("DOMContentLoaded", () => {
    checkbox = document.getElementById("check");
    checkbox.addEventListener("change", () => {
        if (checkbox.checked){
            document.getElementById("code").removeAttribute("hidden");
        }
        else {
            document.getElementById("code").setAttribute("hidden", "true");
        }
    })
})