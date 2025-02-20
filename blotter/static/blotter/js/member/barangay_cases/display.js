

(() => {

    function formatDate(date) {
        return new Date(date).toISOString().split("T")[0];
    }

    document.addEventListener("DOMContentLoaded", () => {
        const updateButtons = document.querySelectorAll(".update-btn");
        
        updateButtons.forEach(button => {
            button.addEventListener("click", () => {
            // Get data attributes
            const dateFiled = button.getAttribute("data-date-filed");
            const caseNum = button.getAttribute("data-case-num");
            const complainant = button.getAttribute("data-complainant");
            const respondent = button.getAttribute("data-respondent");
            const caseType = button.getAttribute("data-case-type");
            const caseFiledId = button.getAttribute("data-case-filed");
            const caseStatus = button.getAttribute("data-case-status");
            const dateSettled = button.getAttribute("data-date-settled");
            const timeSettled = button.getAttribute("data-time-settled");

            // Populate text fields
            document.getElementById("case_num").value = caseNum;
            document.getElementById("complainant").value = complainant;
            document.getElementById("respondent").value = respondent;
        
            // Populate date fields (convert Dec. 15, 2024 to YYYY-MM-DD)
            const formattedDateFiled = formatDate(dateFiled);
            document.getElementById("date_filed").value = formattedDateFiled;
                    

            const formattedDateSetteled = formatDate(dateSettled);
            document.getElementById("date_settled").value = formattedDateSetteled;
        
            // Handle "None" values for date/time settled
            document.getElementById("date_settled").value = dateSettled !== "None" ? new Date(dateSettled).toISOString().split("T")[0] : "";
            document.getElementById("time_settled").value = timeSettled !== "None" ? timeSettled : "";
        
            
            const criminal_case = document.getElementById("case_type_0").value;
            const civil_case = document.getElementById("case_type_1").value;

            const caseTypeRadios = document.getElementsByName("case_type");

            caseTypeRadios.forEach(radio => {
                if (radio.value === caseType) {
                radio.checked = true;
                }
            });

            const caseFileSelectTag = document.getElementById("case_filed");

            for (let i = 0; i < caseFileSelectTag.options.length; i++) {
                if (caseFileSelectTag.options[i].value === caseFiledId) {
                caseFileSelectTag.options[i].selected = true;
                }
            }

            const caseStatusSelectTag = document.getElementById('case_status');
            
            for (let i = 0; i < caseStatusSelectTag.options.length; i++) {
                if (caseStatusSelectTag.options[i].value === caseStatus) {
                caseStatusSelectTag.options[i].selected = true;
                }
            }
            });
        });
        });
})();