document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 10; // Number of rows per page
    const table = document.getElementById("table");
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    const pagination = document.getElementById("pagination");

    // References to Previous and Next buttons
    const prevButton = pagination.querySelector(".page-item:first-child");
    const nextButton = pagination.querySelector(".page-item:last-child");

    // Function to show a specific page
    function showPage(page) {
        rows.forEach((row, index) => {
            row.style.display = index >= (page - 1) * rowsPerPage && index < page * rowsPerPage ? "" : "none";
        });

        // Enable/disable Previous and Next buttons
        prevButton.classList.toggle("disabled", page === 1);
        nextButton.classList.toggle("disabled", page === totalPages);

        // Update pagination numbers
        updatePaginationNumbers(page);
    }

    // Function to update pagination numbers dynamically
    function updatePaginationNumbers(currentPage) {
        // Clear existing pagination numbers
        Array.from(pagination.querySelectorAll(".page-item")).forEach((item, idx) => {
            if (idx > 0 && item !== nextButton) {
                item.remove();
            }
        });

        // Determine the range of page numbers to display
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, startPage + 4);

        // Add page numbers within the range
        for (let i = startPage; i <= endPage; i++) {
            const li = document.createElement("li");
            li.className = `page-item ${i === currentPage ? "active" : ""}`;
            const link = document.createElement("a");
            link.className = "page-link";
            link.href = "#";
            link.textContent = i;

            link.addEventListener("click", function (e) {
                e.preventDefault();
                showPage(i);
            });

            li.appendChild(link);
            pagination.insertBefore(li, nextButton);
        }
    }

    // Add event listeners for Previous and Next buttons
    prevButton.querySelector("a").addEventListener("click", function (e) {
        e.preventDefault();
        const currentPage = parseInt(pagination.querySelector(".page-item.active a").textContent, 10);
        showPage(Math.max(1, currentPage - 1));
    });

    nextButton.querySelector("a").addEventListener("click", function (e) {
        e.preventDefault();
        const currentPage = parseInt(pagination.querySelector(".page-item.active a").textContent, 10);
        showPage(Math.min(totalPages, currentPage + 1));
    });

    // Initialize pagination and show the first page
    updatePaginationNumbers(1);
    showPage(1);
});
