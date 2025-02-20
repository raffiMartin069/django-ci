export async function post(url, method, data, csrftoken) {
    try {
        const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
            body: JSON.stringify(data)
        })

        if(!response.ok) {
            throw new Error(response.statusText);
        }
        const json = await response.json();
        return json;
    } catch (error) {
        throw new Error(error);
    }
}

