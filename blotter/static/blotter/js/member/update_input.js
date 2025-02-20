document.addEventListener("DOMContentLoaded", function () {
    const btnUpdateInfo = document.getElementById("update-btn");
    //const btnClear = document.getElementById("clear-info");
    const btnUpdate = document.getElementById("update-info");
    const inputs = document.querySelectorAll(".modal-body input:not([type='radio'])");
    const selects = document.querySelectorAll(".modal-body select");
    const radioButtons = document.querySelectorAll(".modal-body input[type='radio']");
    const allFields = [...inputs, ...selects, ...radioButtons]; // Combine inputs, selects, and radio buttons into one list

    // Set initial state
    //btnClear.classList.add("d-none");
    btnUpdate.classList.add("d-none");
    allFields.forEach(field => {
        field.setAttribute("readonly", true);
        if (field.tagName.toLowerCase() === "select") {
            field.setAttribute("disabled", true); // Disable select elements
        }
        if (field.type === "radio") {
            field.setAttribute("disabled", true); // Disable radio buttons
        }
    });

    // Handle Update Information button click
    btnUpdateInfo.addEventListener("click", function () {
        btnUpdateInfo.classList.add("d-none");
        //btnClear.classList.remove("d-none");
        btnUpdate.classList.remove("d-none");
        allFields.forEach(field => {
            field.removeAttribute("readonly");
            if (field.tagName.toLowerCase() === "select") {
                field.removeAttribute("disabled"); // Enable select elements
            }
            if (field.type === "radio") {
                field.removeAttribute("disabled"); // Enable radio buttons
            }
        });
    });
});