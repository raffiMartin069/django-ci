document.addEventListener("DOMContentLoaded", function () {
    let updateButton = document.getElementById("update-btn");
    let formFields = document.querySelectorAll("#updateUserForm input, #updateUserForm select");
    let form = document.getElementById("updateUserForm");

    // Function to disable all form fields
    function disableFields() {
        formFields.forEach(field => {
            field.setAttribute("disabled", "true");
        });
        updateButton.textContent = "Update Information";
    }

    // Function to enable all form fields
    function enableFields() {
        formFields.forEach(field => {
            field.removeAttribute("disabled");
        });
        updateButton.textContent = "Save Changes";
    }

    // Function to populate modal fields with user data
    function populateModal(button) {
        try {
            console.log("Button clicked: ", button);

            // Retrieve data attributes from the clicked button
            var userId = button.getAttribute('data-user-id');
            var firstName = button.getAttribute('data-user-firstname');
            var middleName = button.getAttribute('data-user-middlename');
            var lastName = button.getAttribute('data-user-lastname');
            var roleName = button.getAttribute('data-user-role_name');
            var username = button.getAttribute('data-user-username');
            var accountStatus = button.getAttribute('data-user-account_status');

            // Log the retrieved data for debugging
            console.log("User Data Retrieved:", { userId, firstName, middleName, lastName, roleName, username, accountStatus });

            // Populate modal form fields
            document.getElementById("update_user_id").value = userId || '';
            document.querySelector('[name="fname"]').value = firstName || '';
            document.querySelector('[name="mname"]').value = middleName || '';
            document.querySelector('[name="lname"]').value = lastName || '';
            document.querySelector('[name="username"]').value = username || '';
            document.querySelector('[name="role"]').value = roleName || '';
            document.querySelector('[name="account_status"]').value = accountStatus || '';

            // Disable fields initially
            disableFields();

        } catch (error) {
            console.error("Error populating the modal:", error);
            alert("An error occurred while populating the modal. Check the console for details.");
        }
    }

    // Attach event listener to all "Update" buttons
    document.querySelectorAll('.btn-update-res').forEach(button => {
        button.addEventListener('click', function () {
            console.log("Update button clicked.");
            populateModal(this);
        });
    });

    // Handle click event on "Update Information / Save Changes" button
    updateButton.addEventListener("click", function (event) {
        if (updateButton.textContent === "Update Information") {
            event.preventDefault(); // Prevent accidental form submission
            enableFields();
        } else {
            // Submit the form via AJAX
            event.preventDefault();
            let formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData
            })
            .then(response => response.json()) // Assuming Django returns JSON response
            .then(data => {
                if (data.success) {
                    alert("User updated successfully!");
                    disableFields(); // Disable fields again after successful update
                } else {
                    alert("Error updating user. Please check input fields.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            });
        }
    });

});
