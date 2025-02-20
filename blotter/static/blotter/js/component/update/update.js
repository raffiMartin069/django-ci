import {post} from "../../api/post.js";
import {getCookie} from "../../utilities/csrftoken.js";

function validate_case_type_input() {
    // check if case type has a value or not, if not, set it to the default value
    let case_type = document.getElementById('case_type_0').value
    if (case_type === null || case_type === "None" || case_type === undefined) {
        case_type = document.getElementById('case_type_1').value
    }
    return case_type;
}

function validate_residency_input() {
    let resident = document.getElementById('complainant_resident_0').value
    if (resident === null || resident === "None" || resident === undefined) {
        resident = document.getElementById('complainant_resident_1').value
    }
    return resident;
}

function getIds() {
    try {
        const current_case_number = document.getElementById('current_case_number').value
        const date_filed = document.getElementById('date_filed').value
        const case_num = document.getElementById('case_num').value
        const complainant_fname = document.getElementById('complainant_fname').value
        const complainant_mname = document.getElementById('complainant_mname').value
        const complainant_lname = document.getElementById('complainant_lname').value
        const respondent_fname = document.getElementById('respondent_fname').value
        const respondent_mname = document.getElementById('respondent_mname').value
        const respondent_lname = document.getElementById('respondent_lname').value
        const case_status = document.getElementById('case_status').value
        const date_settled = document.getElementById('date_settled').value
        const case_type = validate_case_type_input();
        const case_filed = document.getElementById('case_filed').value
        const resident = validate_residency_input();
        return {
            current_case_number, date_filed, case_num, complainant_fname,
            complainant_mname, complainant_lname, respondent_fname, respondent_mname,
            respondent_lname, case_status, date_settled, case_type, case_filed, resident
        }
    } catch (error) {
        return null;
    }
}

export function updateCase() {
    try {
        const update_case_form = document.getElementById('update_modal_form');
        if (update_case_form === null || update_case_form === undefined) {
            return;
        }
        const token = getCookie('csrftoken');
        update_case_form.addEventListener('submit', async (e) => {
            try {
                const data = getIds();
                await post('/blotter/update-case/', 'POST', data, token);
            } catch (error) {
                console.error('Update failed:', error);
                alert('Network/request error. Please try again.');
            }
        });
    } catch (error) {
        console.error(error);
    }
}