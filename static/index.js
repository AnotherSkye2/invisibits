async function logSubmit(event) {
    event.preventDefault();
    try {
        window.location.href = "http://localhost:8001/generate"
    } catch(err) {
        console.error(err)
    }
}

async function UploadHandler() {
    if (this.files && this.files[0]) {
        var img = document.querySelector('img');
        img.onload = () => {
            URL.revokeObjectURL(img.src);  // no longer needed, free memory
        }
        img.src = URL.createObjectURL(this.files[0]);

        imgForm = document.querySelector("#img-form")
        const formData = new FormData(imgForm)
        const fileName = input.value.split("\\")[-1]
        console.log(formData)
        try {
            const response = await fetch(`./upload?fileName=${fileName}`, {
                method: "POST",
                body: formData
            })

            if(!response.ok) throw new Error(response.statusText)
            console.log(response.statusText)
        } catch(err) {
            console.error(err)
        }
    }
}

async function EncodeHandler(e) {
    e.preventDefault()
    const input = document.querySelector('input[type="file"]')
    const textForm = document.querySelector("#text-form")
    const formData = new FormData(textForm)
    const fileNameArray = input.value.split("\\")
    const fileName = fileNameArray[fileNameArray.length-1]
    console.log(formData, fileName)
    try {
        const response = await fetch(`./encode?fileName=${fileName}`, {
            method: "POST",
            body: formData
        })

        if(!response.ok) throw new Error(response.statusText)
        console.log(response.statusText)
    } catch(err) {
        console.error(err)
    }
    
}

window.onload = (event) => {   
    console.log("page is fully loaded");
    const input = document.querySelector('input[type="file"]')
    const textForm = document.querySelector("#text-form")
    console.log(input)
    input.addEventListener('change', UploadHandler)
    textForm.addEventListener('submit', EncodeHandler)
    // const form = document.getElementById("form");
    // form.addEventListener("submit", logSubmit);
}

