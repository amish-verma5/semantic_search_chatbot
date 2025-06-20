let queryEl = document.getElementById("text-box")
let responseEl = document.getElementById("inside_text")
let bodyEl = document.getElementById("body")
let genButton = document.getElementById("gen-button")

queryEl.addEventListener("keydown",
    function (event) {
        if (event.key == "Enter" && !event.shiftKey) {
            event.preventDefault();
            genButton.click();
        }
    }
);

function generateResponse() {
    if (queryEl.value.trim() !== "") {
        let query = document.createElement("p");
        query.textContent = queryEl.value;
        query.id = "inside_text"
        ques=queryEl.value;
        queryEl.value = "";
        bodyEl.appendChild(query);

        let ans = document.createElement("p");
        ans.id = "inside_text";
        ans.textContent = "Working over your query ✅...";
        bodyEl.appendChild(ans);
        bodyEl.scrollTop = bodyEl.scrollHeight;

        // Step-by-step status messages with timing
        setTimeout(() => {
            ans.textContent = "You're into semantic search 🔎...";
        }, 4000);
        setTimeout(() => {
            ans.textContent = "Your chosen k is: 5";
        }, 8000);
        setTimeout(() => {
            ans.textContent = "Analysing the retrieved paragraphs 🕵🏻...";
        }, 8000);
        setTimeout(() => {
            ans.textContent = "Our wizard is casting the ‘load’ spell… please hold your applause.";
        }, 5000);
        setTimeout(() => {
            sendQ(ans,ques); // Call backend after all steps
        }, 5000);
    }
}

function sendQ(ans,ques) {
    let query = ques;

    fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // ✅ Needed for FastAPI to parse JSON
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        // let ans = document.createElement("p")
        ans.textContent = data.reply;
        // ans.id = "inside_text";
        // bodyEl.appendChild(ans);
    });
}



// if($("p").hasClass("2343")){
//     $("p").remove(".2343");
// }