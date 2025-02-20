function populateModal(button) {
    try {
      // Debugging log to confirm the button being clicked
      console.log("Button clicked: ", button);
  
      // Retrieve data attributes from the button
      var residentId = button.getAttribute('data-resident-id');
      var firstName = button.getAttribute('data-resident-firstname');
      var middleName = button.getAttribute('data-resident-middlename');
      var lastName = button.getAttribute('data-resident-lastname');
      var street = button.getAttribute('data-resident-street');
      var purok = button.getAttribute('data-resident-purok');
      var precinctNum = button.getAttribute('data-resident-precinct');
      var classification = button.getAttribute('data-resident-classification');
      var status = button.getAttribute('data-resident-status');
  
      // Log the retrieved data
      console.log("Resident Data Retrieved:");
      console.log("ID:", residentId);
      console.log("First Name:", firstName);
      console.log("Middle Name:", middleName);
      console.log("Last Name:", lastName);
      console.log("Street:", street);
      console.log("Purok:", purok);
      console.log("Precinct Number:", precinctNum);
      console.log("Classification:", classification);
      console.log("Status:", status);
  
      var fnameField = document.getElementById('update_fname');
      var mnameField = document.getElementById('update_mname');
      var lnameField = document.getElementById('update_lname');
      var streetField = document.getElementById('update_street');
      var purokField = document.getElementById('update_purok');
      var precinctField = document.getElementById('update_precint_num');
      var classificationField = document.getElementById('update_classification');
      var statusField = document.getElementById('update_status');
      var residentIdField = document.getElementById('update_resident_id');
  
      // to be fixed
      fnameField.value = firstName || '';
      mnameField.value = middleName || '';
      lnameField.value = lastName || '';
      streetField.value = street || '';
      purokField.value = purok || '';
      precinctField.value = precinctNum || '';
      classificationField.value = classification|| '';
      residentIdField.value = residentId || '';
      statusField.value = status || '';
    } catch (error) {
      console.error("Error populating the modal:", error);
      alert("An error occurred while populating the modal. Check the console for more details.");
    }
  }
  
  document.querySelectorAll('.btn-update-res').forEach(button => {
    button.addEventListener('click', function() {
      console.log("Update button clicked.");
      populateModal(this);
    });
  });
  
  document.getElementById('update-btn').addEventListener('click', function() {
      document.getElementById('updateResidentForm').submit();
    });
  
  