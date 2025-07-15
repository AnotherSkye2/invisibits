async function logSubmit(event) {
    event.preventDefault();
    try {
        window.location.href = "http://localhost:8001/generate"
    } catch(err) {
        console.error(err)
    }
}

window.onload = (event) => {   
    console.log("page is fully loaded");
    const form = document.getElementById("form");
    form.addEventListener("submit", logSubmit);
}