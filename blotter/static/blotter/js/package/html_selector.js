export function PageSelector(data_page, jsPath, moduleFunction) {
    const pageElement = document.querySelector('[data-page]');
    if (pageElement) {
        const page = pageElement.getAttribute('data-page');
        if (page === data_page) {
            import(jsPath).then(module => {
                module[moduleFunction]();
            }).catch(err => {
                console.error(`Failed to load module ${jsPath}:`, err);
            });
        }
    }
}