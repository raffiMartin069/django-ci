import { PageSelector } from './package/html_selector.js';
import {removeCase} from "./component/barangay_cases/delete_case.js";

document.addEventListener('DOMContentLoaded', () => {
    PageSelector('barangay-cases', '../component/barangay_cases/barangay_cases.js', 'barangayCases');
    PageSelector('barangay-cases', '../component/barangay_cases/delete_case.js', 'removeCase');

    PageSelector('member_home_form', '../component/barangay_cases/barangay_cases.js', 'barangayCases');

    PageSelector('upload_brgy_cases', '../component/barangay_cases/barangay_cases.js', 'barangayCases');

    PageSelector('manage_account', '../component/manage_account.js', 'manageAccoutnView');

    PageSelector('upload_brgy_cases', '../pages/upload_case_page.js', 'uploadCasesPage');
});