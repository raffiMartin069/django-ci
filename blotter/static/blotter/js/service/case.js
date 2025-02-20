export class CaseService {

    constructor (update_data) {
        this.update_data = update_data;
    }

    validateAttributes() {
        for (let i = 0; i < this.update_data.length; i++) {
            if (this.update_data[i] === null || this.update_data[i] === "None" || this.update_data[i] === undefined) {
                throw new Error(`The attribute at index ${i} is not found on the page`);
                return;
            }
            console.log(this.update_data[i]);
        }
    }
}