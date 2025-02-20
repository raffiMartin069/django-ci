import {populateRadioButtons} from '../../utilities/radio.js';
import {populateSelectTags} from '../../utilities/selectTag.js';
import {convert12HourTo24Hour} from '../../utilities/twentyFourHourFormat.js';

function getAttribs(button) {
    try {
        const dateFiled = button.getAttribute("data-date-filed");
        const timeFiled = button.getAttribute("data-case-time-filed")
        const caseNum = button.getAttribute("data-case-num");
        const complainant_fname = button.getAttribute("data-complainant_fname");
        const complainant_mname = button.getAttribute("data-complainant_mname");
        const complainant_lname = button.getAttribute("data-complainant_lname");
        const respondent_fname = button.getAttribute("data-respondent_fname");
        const respondent_mname = button.getAttribute("data-respondent_mname");
        const respondent_lname = button.getAttribute("data-respondent_lname");
        const caseType = button.getAttribute("data-case-type");
        const caseFiledId = button.getAttribute("data-case-filed");
        const caseStatus = button.getAttribute("data-case-status");
        const dateSettled = button.getAttribute("data-date-settled");
        const timeSettled = button.getAttribute("data-time-settled");
        const current_case_number = button.getAttribute("data-current_case_number");
        const is_complainant_resident = button.getAttribute("data-is_complainant_resident");
        return {
            dateFiled, caseNum, complainant_fname,
            complainant_mname, complainant_lname, respondent_fname,
            respondent_mname, respondent_lname, caseType,
            caseFiledId, caseStatus, dateSettled,
            timeSettled, current_case_number, is_complainant_resident,
            timeFiled
        };
    } catch (error) {
        console.error(error);
    }
}

function residence(attribs) {
    let residenceStatus = null;

    if (attribs === null || attribs === "None" || attribs === undefined) {
        console.error("The residence status is not found on the page");
        return;
    }

    if (attribs === "True") {
        residenceStatus = "Resident";
    } else {
        residenceStatus = "Non-resident";
    }
    return residenceStatus;
}

function validateAttributes(attribs) {
    for (let i = 0; i < attribs.length; i++) {
        if (attribs[i] === null || attribs[i] === "None" || attribs[i] === undefined) {
            throw new Error(`The attribute at index ${i} is not found on the page`);
            return;
        }
        console.log(attribs[i]);
    }
}

export function barangayCases() {
    try {
        const updateBtns = document.querySelectorAll(".update-btn");

        if (updateBtns === null || updateBtns === undefined) {
            console.error("The update button is not found on the page");
            return;
        }

        updateBtns.forEach((btn) => {
            btn.addEventListener("click", () => {
                const attribs = getAttribs(btn);
                document.getElementById("case_num").value = attribs.caseNum;
                document.getElementById("complainant_fname").value = attribs.complainant_fname;
                document.getElementById("complainant_mname").value = attribs.complainant_mname;
                document.getElementById("complainant_lname").value = attribs.complainant_lname;
                document.getElementById("respondent_fname").value = attribs.respondent_fname;
                document.getElementById("respondent_mname").value = attribs.respondent_mname;
                document.getElementById("respondent_lname").value = attribs.respondent_lname;
                document.getElementById("current_case_number").value = attribs.current_case_number;
                document.getElementById("date_filed").value = attribs.dateFiled !== "None" ? new Date(attribs.dateFiled).toLocaleDateString('en-CA') : "";
                document.getElementById("time_filed").value = convert12HourTo24Hour(attribs.timeFiled);
                document.getElementById("date_settled").value = attribs.dateSettled !== "None" ?
                    new Date(attribs.dateSettled).toLocaleDateString('en-CA') : "";
                document.getElementById("time_settled").value = convert12HourTo24Hour(attribs.timeSettled);

                const caseTypeRadios = document.getElementsByName("case_type");
                populateRadioButtons(caseTypeRadios, attribs.caseType);

                const caseFileSelectTag = document.getElementById("case_filed");
                populateSelectTags(caseFileSelectTag, attribs.caseFiledId);

                const caseStatusSelectTag = document.getElementById("case_status");
                populateSelectTags(caseStatusSelectTag, attribs.caseStatus);

                const isComplainantResidentRadios = document.getElementsByName("complainant_resident");
                const status = attribs.is_complainant_resident;
                const residenceStatus = residence(status);
                populateRadioButtons(isComplainantResidentRadios, residenceStatus);
            });
        });
    } catch (error) {
        console.error(error);
    }
}
