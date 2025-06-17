async function logSubmit(event) {
    event.preventDefault();
    try {
        const response = await fetch('./generate')
        if(!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json()
        console.log(data)
    } catch(err) {
        console.error(err)
    }
}

window.onload = (event) => {   
    console.log("page is fully loaded");
    const form = document.getElementById("form");
    form.addEventListener("submit", logSubmit);
}