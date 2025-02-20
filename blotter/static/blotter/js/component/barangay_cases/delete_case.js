export function removeCase() {
    try {
        const removeBtn = document.querySelectorAll(".btn-remove");

        if (removeBtn === null || removeBtn === undefined) {
            console.error("The delete button is not found on the page");
            return;
        }

        removeBtn.forEach((btn) => {
            btn.addEventListener("click", () => {
                const caseNumber = btn.getAttribute("data-bs-case-number");

                if (caseNumber === null || caseNumber === undefined) {
                    console.error("The case number is not found on the page");
                    return;
                }

                const caseNumberInput = document.getElementById('case_number');

                if (caseNumberInput === null || caseNumberInput === undefined) {
                    console.error("The case number input is not found on the page");
                    return;
                }

                caseNumberInput.value = caseNumber;
            })
        });

    } catch (error) {
        console.error(error);
    }
}