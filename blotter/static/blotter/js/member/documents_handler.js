function addDocumentRow() {
    // Get the selected document from the dropdown
    const select = document.getElementById('case_type');
    document.addEventListener('change', () => {
        const selectedValue = select.value;

        // Check if the user has selected a valid option
        if (selectedValue) {
            // Reference the table body
            const tableBody = document.getElementById('documentsTableBody');

            // Create a new row
            const newRow = document.createElement('tr');
            newRow.classList.add('table-row-height');

            // Add the cells
            newRow.innerHTML = `
                <td>${selectedValue}</td>
                <td>
                    <button type="button" class="btn btn-upload" title="Upload Image">Upload</button>
                </td>
                <td>No File Uploaded</td>
                <td>
                    <div class="button-table-container col-lg-12 col-md-8 col-sm-10 justify-content-start">
                        <button type="button" id="uploadBtn" class="btn btn-image" data-bs-toggle="modal" data-bs-target="#image_uploaded">
                            <i class="fa-solid fa-images"></i>
                        </button>
                        <button type="button" class="btn btn-remove" data-bs-toggle="modal" data-bs-target="#remove">
                            <i class="fa-solid fa-circle-xmark"></i>
                        </button>
                    </div>
                </td>
            `;

            // Append the new row to the table body
            tableBody.appendChild(newRow);

            // Optionally reset the dropdown to its default state
            select.value = '';
        }
    })
}
