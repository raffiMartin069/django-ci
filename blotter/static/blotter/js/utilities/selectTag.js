export function populateSelectTags(selectTags, optionId) {
    if (selectTags === null || selectTags === undefined) {
        throw new Error("The select tags are not found on the page");
    }

    if (optionId === null || optionId === undefined) {
        throw new Error("The option id is not found on the page");
    }

    for (let i = 0; i < selectTags.options.length; i++) {
        if (selectTags.options[i].value === optionId) {
            selectTags.options[i].selected = true;
        }
    }
    return selectTags;
}