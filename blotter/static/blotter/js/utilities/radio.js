export function populateRadioButtons(radios, radioValue) {
    if (radios === null || radios === undefined) {
        throw new Error("The radio buttons are not found on the page");
    }

    if (radioValue === null || radioValue === undefined) {
        throw new Error("The radio value is not found on the page");
    }

    try {
        radios.forEach((radio) => {
            if (radio.value === radioValue) {
                radio.checked = true;
            }
        });
        return radios;
    } catch (error) {
        throw new Error(error);
    }
}