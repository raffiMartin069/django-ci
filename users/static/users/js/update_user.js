document.addEventListener("DOMContentLoaded", function () {
    let updateButton = document.getElementById("update-btn");
    let formFields = document.querySelectorAll("#updateUserForm input, #updateUserForm select");
    let form = document.getElementById("updateUserForm");

    // Function to disable form fields
    function disableFields() {
        formFields.forEach(field => {
            field.setAttribute("disabled", "true");
        });
        updateButton.textContent = "Update Information";
    }

    // Function to enable form fields
    function enableFields() {
        formFields.forEach(field => {
            field.removeAttribute("disabled");
        });
        updateButton.textContent = "Save Changes";
    }

    // Function to populate modal fields
    function populateModal(button) {
        try {
            // console.log("Button clicked: ", button);

            // Retrieve data attributes from the button
            var userId = button.getAttribute('data-user-id');
            var firstName = button.getAttribute('data-user-firstname');
            var middleName = button.getAttribute('data-user-middlename');
            var lastName = button.getAttribute('data-user-lastname');
            var roleName = button.getAttribute('data-user-role_name');
            var username = button.getAttribute('data-user-username');
            var accountStatus = button.getAttribute('data-user-account_status');

            // Log the retrieved data
            // console.log("User Data Retrieved:", { userId, firstName, middleName, lastName, roleName, username, accountStatus });

            // Map the data to the modal fields
            document.getElementById("update_user_id").value = userId || '';
            document.querySelector('[name="fname"]').value = firstName || '';
            document.querySelector('[name="mname"]').value = middleName || '';
            document.querySelector('[name="lname"]').value = lastName || '';
            document.querySelector('[name="username"]').value = username || '';
            document.querySelector('[name="role"]').value = roleName || '';
            document.querySelector('[name="account_status"]').value = accountStatus || '';

            // Disable all fields initially
            disableFields();

        } catch (error) {
            console.error("Error populating the modal:", error);
            alert("An error occurred while populating the modal. Check the console for more details.");
        }
    }

    // Attach click listeners to all update buttons
    document.querySelectorAll('.btn-update-res').forEach(button => {
        button.addEventListener('click', function () {
            console.log("Update button clicked.");
            populateModal(this);
        });
    });

    // Toggle between enabling/disabling form fields and submit form when saving
    updateButton.addEventListener("click", function (event) {
        if (updateButton.textContent === "Update Information") {
            event.preventDefault(); // Prevent accidental submission
            enableFields();
        } else {
            // Submit form via AJAX
            event.preventDefault();
            let formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("User updated successfully!");
                    disableFields(); // Disable fields again after successful update
                    window.location.reload(); // **Reload the page**
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
