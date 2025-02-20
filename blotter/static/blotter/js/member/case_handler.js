(() => {
    document.addEventListener('DOMContentLoaded', function () {
        const caseFiledDropdown = document.getElementById('case_filed');
        const caseTypeRadios = document.getElementsByName('case_type');

// Case options
        const civilCases = [
            {value: '8', text: 'Collection of Sum of Money'},
            {value: '9', text: 'Ejectment'},
            {value: '10', text: 'Damages (Reimbursement)'},
        ];

        const criminalCases = [
            {value: '1', text: 'Oral Defamation'},
            {value: '2', text: 'Slight Physical Injury'},
            {value: '3', text: 'Theft'},
            {value: '4', text: 'Malicious Mischief'},
            {value: '5', text: 'Estafa'},
            {value: '6', text: 'Trespass to Dwelling'},
            {value: '7', text: 'Illegal Trespassing'},
        ];

// Populate dropdown based on selected case type
        function populateCases(cases) {
            caseFiledDropdown.innerHTML = '<option value="" disabled selected>Select Case Filed</option>';
            cases.forEach(caseItem => {
                const option = document.createElement('option');
                option.value = caseItem.value;
                option.textContent = caseItem.text;
                caseFiledDropdown.appendChild(option);
            });
        }

// Event listeners for radio buttons
        caseTypeRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                if (radio.value === '1') {
                    populateCases(civilCases);
                } else if (radio.value === '2') {
                    populateCases(criminalCases);
                }
            });
        });

    })
})();