import {populateRadioButtons} from '../utilities/radio.js';
import {populateSelectTags} from "../utilities/selectTag.js";

function getAttribs(button) {
    const fname = button.getAttribute("data-first_name");
    const mname = button.getAttribute("data-middle_name");
    const lname = button.getAttribute("data-last_name");
    const uname = button.getAttribute("data-username");
    const user_id = button.getAttribute("data-user_key");
    const user_role = button.getAttribute("data-role_name");
    const is_active = button.getAttribute("data-is_active");
    return {
        fname, mname, lname, is_active, uname, user_id, user_role
    }
}

function modalBtnValidation(modalBtn) {
    if (modalBtn.length === 0) {
        throw new Error("No buttons found");
        return;
    }

    if (modalBtn === null) {
        throw new Error("No buttons found");
        return;
    }

    if (modalBtn === undefined) {
        throw new Error("No buttons found");
        return;
    }

    if (modalBtn === "") {
        throw new Error("No buttons found");
        return;
    }
}

export function manageAccoutnView() {
    try {
        const modalBtn = document.querySelectorAll(".info_btn, .update_btn");
        modalBtnValidation(modalBtn);

        modalBtn.forEach((btn) => {
            btn.addEventListener('click', () => {
                const attribs = getAttribs(btn);
                document.getElementById("info_fname").value = attribs.fname;
                document.getElementById("info_mname").value = attribs.mname;
                document.getElementById("info_lname").value = attribs.lname;
                document.getElementById("info_username").value = attribs.uname;
                const info_radio = document.getElementsByName('account_status');
                populateRadioButtons(info_radio, attribs.is_active);
                const infoSelectTag = document.getElementById('info_account_roles')
                populateSelectTags(infoSelectTag, attribs.user_role);
                document.getElementById("update_fname").value = attribs.fname;
                document.getElementById("update_mname").value = attribs.mname;
                document.getElementById("update_lname").value = attribs.lname;
                document.getElementById("update_username").value = attribs.uname;
                document.getElementById("account_id").value = attribs.user_id;
                const update_radio = document.getElementsByName('account_status');
                populateRadioButtons(update_radio, attribs.is_active);
                const updateSelectTag = document.getElementById('update_account_roles')
                populateSelectTags(updateSelectTag, attribs.user_role);
            });
        });
    } catch (error) {
        console.error(error);
    }
}