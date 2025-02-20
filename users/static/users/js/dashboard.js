document.addEventListener("DOMContentLoaded", function () {
    const monthFilter = document.getElementById("monthFilter");
    const yearFilter = document.getElementById("yearFilter");

    // Fetch initial data on page load
    fetchFilteredData();

    function fetchFilteredData() {
        const selectedMonth = monthFilter.value;
        const selectedYear = yearFilter.value;

        let url = new URL(window.location.href);
        url.searchParams.set("month", selectedMonth);
        url.searchParams.set("year", selectedYear);

        fetch(url.toString(), {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById("totalCases").textContent = data.total_cases_this_month;
                document.getElementById("casesReported").textContent = data.cases_reported_this_year;
                document.getElementById("monthLabel").textContent = `(${data.current_month})`;
                document.getElementById("yearLabel").textContent = `(${data.current_year})`;

                updateChart(data.civil_case_count, data.criminal_case_count);
            })
            .catch(error => console.error("Error fetching data:", error));
    }

    function updateChart(civilCases, criminalCases) {
        if (window.caseChart) {
            window.caseChart.destroy();
        }

        const ctx = document.getElementById("caseDistributionChart").getContext("2d");
        window.caseChart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["Civil Cases", "Criminal Cases"],
                datasets: [{
                    data: [civilCases, criminalCases],
                    backgroundColor: ["#FF8C00", "#8B0000"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: "bottom",  // 👈 Legend now appears at the bottom
                    },
                    title: {
                        display: true,
                        text: `Civil and Criminal Cases for ${document.getElementById("yearLabel").textContent}`
                    }
                }
            }
        });
    }

    monthFilter.addEventListener("change", fetchFilteredData);
    yearFilter.addEventListener("change", fetchFilteredData);
});
