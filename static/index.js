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
    input = document.querySelector('input[type="file"]')
    console.log(input)
    input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            var img = document.querySelector('img');
            img.onload = () => {
                URL.revokeObjectURL(img.src);  // no longer needed, free memory
            }
            img.src = URL.createObjectURL(this.files[0]);

            imgForm = document.querySelector("form")
            const formData = new FormData(imgForm)

            console.log(formData)
            fetch(`./upload?fileName=${input.value}`, {
                method: "POST",
                body: formData
            })

            .then(response => {
                if(!response.ok) throw Error(response.statusText)
                console.log(response.statusText)
            })
        }
    });
    // const form = document.getElementById("form");
    // form.addEventListener("submit", logSubmit);
}