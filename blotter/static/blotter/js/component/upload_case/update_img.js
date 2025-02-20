export function UpdateFormImage() {
    try {
        const updateBtn = document.querySelectorAll('.btn-update');

        if (updateBtn === null || updateBtn === undefined) {
            console.error("The update button is not found on the page");
            return;
        }

        updateBtn.forEach((btn) => {
            btn.addEventListener('click', () => {
                let doc_id = btn.getAttribute('data-doc_id');

                if (doc_id === null || doc_id === undefined) {
                    console.error("The document id is not found on the button");
                    return;
                }

                let form_input = document.getElementById('update_doc_id');

                if (form_input === null || form_input === undefined) {
                    console.error("The form input is not found on the page");
                    return;
                }

                form_input.value = doc_id;
            })
        })
    } catch (error) {
        console.error("Something went wrong while updating the image ", error);
    }
}