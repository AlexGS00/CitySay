document.addEventListener("DOMContentLoaded", function() {
    num_options = document.getElementById("num-options");
    addBtn = document.getElementById("add-btn");
    removeBtn = document.getElementById("rm-btn");
    optionsSection = document.getElementById("options");

    addBtn.addEventListener("click", function() {
        newOptionNum = parseInt(num_options.value) + 1;
        num_options.value = newOptionNum;
        var newOption = document.createElement("div");
        newOption.className = "option";
        newOption.innerHTML = `
        <label for="option-${newOptionNum}" class="form-label">Optiunea ${newOptionNum}:</label>
        <input class="option-input" name="option-${newOptionNum}" id="option-${newOptionNum}" type="text" autocomplete="off" placeholder="Optiunea ${newOptionNum}" class="option-input"></input>
        `
        optionsSection.appendChild(newOption)

    });
    removeBtn.addEventListener("click", function() {
        if (parseInt(num_options.value) > 2) {
            var lastOption = optionsSection.lastElementChild;
            optionsSection.removeChild(lastOption);
            num_options.value = parseInt(num_options.value) - 1;
        } else {
            alert("Trebuie sa existe cel putin doua optiuni!");
        }
    });
});