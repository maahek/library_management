
document.addEventListener("DOMContentLoaded", function () {

    const issued = {{ issued_count }};
    const due = {{ due_count }};

    const ctx = document.getElementById("bookChart").getContext("2d");
alert("Chart script running");

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Issued", "Due"],
            datasets: [{
                data: [issued, due],
                backgroundColor: ["#6d4c41", "#bcaaa4"]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

});

