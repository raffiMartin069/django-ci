export function ImageUploaded() {
    // Select all buttons with the `btn-image` class
    const uploadedImgButtons = document.querySelectorAll('.btn-image');

    uploadedImgButtons.forEach((button) => {
        button.addEventListener('click', (e) => {
            // Get the image URL from the button's `data-image` attribute
            const img = button.getAttribute('data-image');

            // Update the modal's image src
            const display = document.getElementById('img_uploaded');
            display.src = img;
        });
    });
}
