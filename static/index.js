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
        var img = document.querySelector(`div[id=${this.id}] img`);
        img.onload = () => {
            URL.revokeObjectURL(img.src);  // no longer needed, free memory
        }
        img.src = URL.createObjectURL(this.files[0]);

        const imgForm = document.querySelector(`div[id=${this.id}] #img-form`)
        const input = document.querySelector(`div[id=${this.id}] input[type="file"]`)
        console.log(imgForm, input, this.files, this.id, img)
        const formData = new FormData(imgForm)
        const fileNameArray = input.value.split("\\")
        const fullFileName = fileNameArray[fileNameArray.length-1]
        console.log(formData, imgForm, fullFileName)
        try {
            const response = await fetch(`./upload?fileName=${fullFileName}`, {
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
    const input = document.querySelector('div[id="encode"] input[type="file"]')
    const textForm = document.querySelector('div[id="encode"] #text-form')
    const formData = new FormData(textForm)
    const fileNameArray = input.value.split("\\")
    const fullFileName = fileNameArray[fileNameArray.length-1]
    console.log(formData, fullFileName)
    try {
        const response = await fetch(`./encode?fileName=${fullFileName}`, {
            method: "POST",
            body: formData
        })

        if(!response.ok) throw new Error(response.statusText)
        console.log(response.statusText)
    } catch(err) {
        console.error(err)
    }
    const fileDownloadNameArray = fullFileName.split('.')
    const fileExtension = fileDownloadNameArray[1]
    const fileName = fileDownloadNameArray[0]
    window.location.href = `./download?fileName=${fileName+'_steg.'+fileExtension}`
}

async function DecodeHandler(e) {
    e.preventDefault()
    const input = document.querySelector('div[id="decode"] input[type="file"]')
    const fileNameArray = input.value.split("\\")
    const fullFileName = fileNameArray[fileNameArray.length-1]
    console.log(fullFileName)
    try {
        const response = await fetch(`./decode?fileName=${fullFileName}`, {
            method: "POST",
        })
        console.log(response)

        if(!response.ok) throw new Error(response.statusText)
        const data = await response.json()
        console.log(data)
        console.log(response.statusText)
    } catch(err) {
        console.error(err)
    }
}

function DisplayHandler(id) {
    const encodeDiv = document.querySelector(`div[id="encode"]`)
    const decodeDiv = document.querySelector(`div[id="decode"]`)
    if (id == "encode") {
        encodeDiv.hidden = false
        decodeDiv.hidden = true
    } else {
        encodeDiv.hidden = true
        decodeDiv.hidden = false
    }
}

window.onload = (event) => {   
    console.log("page is fully loaded");
    const encodeInput = document.querySelector('div[id="encode"] input[type="file"]')
    const decodeInput = document.querySelector('div[id="decode"] input[type="file"]')
    const textForm = document.querySelector('div[id="encode"] #text-form')
    const imgForm = document.querySelector('div[id="decode"] #img-form')
    const displayButtons = document.getElementsByClassName('display')
    console.log(encodeInput.id)
    encodeInput.id = "encode"
    decodeInput.id = "decode"
    encodeInput.addEventListener('change', UploadHandler)
    decodeInput.addEventListener('change', UploadHandler)
    textForm.addEventListener('submit', EncodeHandler)
    imgForm.addEventListener('submit', DecodeHandler)
    for(let button of displayButtons) {
        button.addEventListener('click', () => DisplayHandler(button.id))
    };
    // const form = document.getElementById("form");
    // form.addEventListener("submit", logSubmit);
}

