export function convert12HourTo24Hour(time12h) {
    try {
        if (!time12h || time12h.toLowerCase() === "none") return "";

        if (time12h.toLowerCase() === "noon") {
            return "12:00";
        }

        if (time12h.toLowerCase() === "midnight") {
            return "00:00";
        }

        const match = time12h.match(/^(\d{1,2})(?::(\d{2}))?\s?([ap]\.?m\.?)$/i);

        if (!match) {
            // Invalid format, return empty string or handle the error as needed
            console.error(`Invalid time format: ${time12h}`);
            return "";
        }

        let hours = parseInt(match[1], 10);
        const minutes = match[2] || "00"; // Default to "00" if minutes are missing
        const ampm = match[3].toLowerCase();

        if (ampm.startsWith("p") && hours !== 12) {
            hours += 12;
        } else if (ampm.startsWith("a") && hours === 12) {
            hours = 0;
        }

        return `${String(hours).padStart(2, "0")}:${minutes}`;
    } catch (error) {
        throw error;
    }
}