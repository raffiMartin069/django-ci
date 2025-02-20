export function addDocumentRow() {
    try {
        const select = document.getElementById('case_type');
        const form_id = document.getElementById('form_name')

        if (!select || select === null || select === undefined || select.length === 0) {
            return;
        }

        select.addEventListener('change', () => {
            const selectedValue = select.value;
            const selectedText = select.options[select.selectedIndex].text;
            if (selectedValue) {
                const tableBody = document.getElementById('documentsTableBody');

                if (!tableBody || tableBody === null || tableBody === undefined) {
                    return;
                }

                let documentExists = isSelected(selectedText, tableBody);

                if (!documentExists) {
                    appendRow(tableBody, selectedText);
                } else {
                    alert('This document is already added!');
                }
                const doc_type = document.getElementById('case_type');
                const docTypeText = doc_type.options[doc_type.selectedIndex].text;
                const formName = document.getElementById('form_name');
                formName.value = docTypeText;
                form_id.value = selectedValue;
                select.value = ''; // Clear the dropdown
            }
        });
    } catch (err) {
        console.error(err);
    }
}

const appendRow = (tableBody, selectedValue) => {
    const newRow = document.createElement('tr');
    newRow.classList.add('table-row-height');
    newRow.innerHTML = `
                    <td>${selectedValue}</td>
                    <td>
                        <form>
                            <button type="button" class="btn btn-upload" data-bs-toggle="modal" data-bs-target="#upload_kp_form_modal" title="Upload Image">Upload</button>
                        </form>
                    </td>
                    <td>No File Uploaded</td>
                    <td>
                        <div class="button-table-container d-flex flex-wrap gap-2">
                            <button type="button" class="btn btn-image" title="Preview Image" data-bs-toggle="modal" data-bs-target="#image_uploaded">
                                <i class="fa-solid fa-images"></i>
                            </button>
                            <button type="button" class="btn btn-remove" title="Remove Document" data-bs-toggle="modal" data-bs-target="#remove">
                                <i class="fa-solid fa-circle-xmark"></i>
                            </button>
                        </div>
                    </td>
                `;
    tableBody.appendChild(newRow);
    return newRow;
}

const isSelected = (selectedValue, tableBody) => {
    let documentExists = false;
    const rows = tableBody.getElementsByTagName('tr');

    if (rows.length === 0) {
        return;
    }

    for (let row of rows) {
        const cells = row.getElementsByTagName('td');
        if (cells[0].innerText === selectedValue) {  // Check the document name (first column)
            documentExists = true;
            break;
        }
    }
    return documentExists;
}
