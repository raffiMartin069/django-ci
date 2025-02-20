function validate_cookie(cookie) {
    if (!cookie) {
        throw new Error('Cookie name is required');
    }
}

export function getCookie(name) {
    try {

        validate_cookie(name);

        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const trimmedCookie = cookie.trim();
                // Check if this cookie starts with the name we want
                if (trimmedCookie.startsWith(`${name}=`)) {
                    cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    } catch (error) {
        throw new Error(error);
    }
}