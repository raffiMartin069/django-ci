import { addDocumentRow } from '../component/upload_case/table.js';
import {UpdateFormImage} from "../component/upload_case/update_img.js";
import { docPrinter } from "../component/barangay_cases/printer.js";

export function uploadCasesPage() {
    addDocumentRow();
    UpdateFormImage();
    window.docPrinter = docPrinter;
}