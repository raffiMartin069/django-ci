document.getElementById('logout').addEventListener('click', function () {
    const confirmation = confirm("Are you sure you want to log out?");
    if (confirmation) {
        window.location.href = "/authentication/logout/";
    }
});

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

