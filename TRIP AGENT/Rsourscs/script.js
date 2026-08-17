const form = document.getElementById("travelForm");

const loading = document.getElementById("loading");
const results = document.getElementById("results");

const userQuery = document.getElementById("userQuery");
const planButton = document.getElementById("planButton");

const answer = document.getElementById("answer");
const flightResults = document.getElementById("flightResults");
const hotelResults = document.getElementById("hotelResults");
const itinerary = document.getElementById("itinerary");

const tripQuery = document.getElementById("tripQuery");
const llmCalls = document.getElementById("llmCalls");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const query = userQuery.value.trim();

    if (!query) {
        return;
    }

    // Show loading
    loading.classList.remove("hidden");
    results.classList.add("hidden");

    planButton.disabled = true;
    planButton.innerHTML = "Planning...";

    window.scrollTo({
        top: loading.offsetTop - 50,
        behavior: "smooth"
    });

    try {

        const response = await fetch("/plan", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                user_input: query
            })

        });


        if (!response.ok) {
            throw new Error("Unable to create travel plan.");
        }


        const data = await response.json();


        // Fill results

        tripQuery.textContent = query;

        answer.textContent = data.answer || "No answer available.";

        flightResults.textContent =
            data.flight_results || "No flight information available.";

        hotelResults.textContent =
            data.hotel_results || "No hotel information available.";

        itinerary.textContent =
            data.itinerary || "No itinerary available.";

        llmCalls.textContent =
            data.llm_calls || 0;


        // Hide loading
        loading.classList.add("hidden");

        // Show results
        results.classList.remove("hidden");

        window.scrollTo({
            top: results.offsetTop - 50,
            behavior: "smooth"
        });


    } catch (error) {

        alert(error.message);

        loading.classList.add("hidden");

    } finally {

        planButton.disabled = false;

        planButton.innerHTML = `
            <span>Plan My Trip</span>
            <span>→</span>
        `;

    }

});


function setQuery(query) {

    userQuery.value = query;

    userQuery.focus();

}


function newTrip() {

    results.classList.add("hidden");

    userQuery.value = "";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}