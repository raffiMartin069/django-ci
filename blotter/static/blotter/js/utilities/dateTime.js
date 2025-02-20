export function formatDateTime(date) {
    try {
        return new Date(date).toISOString().split("T")[0];
    } catch (error) {
        throw error;
    }
}
