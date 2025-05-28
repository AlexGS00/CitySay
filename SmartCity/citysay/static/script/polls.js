document.addEventListener('DOMContentLoaded', function() {

    select = document.getElementById("institutions");

    select.addEventListener("change", function() {
        const selectedOption = select.options[select.selectedIndex];
        fetch(`/institution_polls/${selectedOption.value}`)
        .then(response => response.text())
        .then(html => {
            pollSection = document.getElementById("polls-container");
            pollSection.innerHTML = html;
        })
        .then(() => {
            console.log("Successfully updated polls section");
        })
    });
});