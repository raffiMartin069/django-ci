document.addEventListener("DOMContentLoaded", function () {
  const dashboardButton = document.getElementById("goto-dashboard");

  dashboardButton.addEventListener("click", function () {
      fetch('/users/get_user_role/')
          .then(response => response.json())
          .then(data => {
              if (data.role === 'Admin' || data.role === 'Barangay Captain' || data.role === 'Super Admin') {
                  window.location.href = "/users/a/dashboardstats/";
              } else if (data.role === 'Barangay Clerk') {
                  window.location.href = "/profiling/register_resident/";
              } else if (data.role === 'Lupon President' || data.role === 'Barangay Secretary') {
                  window.location.href = "/users/lupon_president/dashboard/";
              } else if (data.role === 'Guest'){
                  alert("You must be logged in to view the dashboard.");
                  window.location.href = "/authentication/login/"; // Redirect to login page
              }
               else {
                  console.error("Unknown user role:", data.role);
                  alert("Could not determine your dashboard.");
              }
          })
          .catch(error => {
              console.error("Error fetching user role:", error);
              alert("An error occurred. Please try again later.");
          });
  });
});

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const tableRows = document.querySelectorAll("#table tbody tr");

    searchInput.addEventListener("input", function () {
      const searchTerm = searchInput.value.toLowerCase();

      tableRows.forEach(row => {
        // Combine all cell text content from the row into a single string
        const rowText = Array.from(row.querySelectorAll("td"))
          .map(cell => cell.textContent.toLowerCase())
          .join(" ");
        
        // Check if the search term exists in the row text
        if (rowText.includes(searchTerm)) {
          row.style.display = ""; // Show the row
        } else {
          row.style.display = "none"; // Hide the row
        }
      });
    });
  });

  // document.addEventListener("DOMContentLoaded", function () {
  //   const dateInput = document.getElementById("date_logs");
  //   const tableRows = document.querySelectorAll("#table tbody tr");

  //   dateInput.addEventListener("input", function () {
  //       const selectedDate = dateInput.value; // YYYY-MM-DD format

  //       // If no date is selected, show all rows
  //       if (!selectedDate) {
  //           tableRows.forEach(row => {
  //               row.style.display = ""; // Show the row
  //           });
  //           return;
  //       }

  //       tableRows.forEach(row => {
  //           const dateCell = row.querySelector("td:nth-child(4)"); // Get the Date and Time cell
  //           const rowDateTime = dateCell ? dateCell.textContent.trim() : ""; // Full Date and Time string (MM/DD/YYYY HH:MM AM/PM)
  //           const rowDate = rowDateTime.split(" ")[0]; // Extract the date part (MM/DD/YYYY)

  //           // Convert the row date to the same format as the input (YYYY-MM-DD)
  //           const [month, day, year] = rowDate.split("/"); // Split MM/DD/YYYY
  //           const formattedRowDate = `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;

  //           // Compare the selected date with the formatted row date
  //           if (formattedRowDate === selectedDate) {
  //               row.style.display = ""; // Show the row if the dates match
  //           } else {
  //               row.style.display = "none"; // Hide the row if the dates don't match
  //           }
  //       });
  //   });
  // });