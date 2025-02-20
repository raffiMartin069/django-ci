(() => {
    const response = "{{ response|escapejs }}";
        if (response === null || response === "" 
        || response === undefined || response === "None") {
            return;
        }
        if (response === "Form is invalid") {
            return;
        }
        alert(response);
})