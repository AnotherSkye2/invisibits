async function UploadHandler() {
    if (this.files && this.files[0]) {
        var img = document.querySelector(`div[id=${this.id}] img`);
        img.onload = () => {
            URL.revokeObjectURL(img.src);  // no longer needed, free memory
        }
        const maxSizeInMB = 5
        if(this.files[0].size / (1024 ** 2) > maxSizeInMB) {
            DisplayError("File size is too big!")
            return
        }
        
        img.src = URL.createObjectURL(this.files[0]);
        console.log(img, img.height)
        const imgForm = document.querySelector(`div[id=${this.id}] #img-form`)
        const formData = new FormData(imgForm)
        formData.append("fileName", formData.get("imgFile").name)
        formData.delete("inputString")
        console.log(...formData, imgForm)
        try {
            const response = await fetch(`./upload?`, {
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
    const imgInput = document.querySelector('div[id="encode"] input[type="file"]')
    const imgForm = document.querySelector('div[id="encode"] #img-form')
    const formData = new FormData(imgForm)
    const inputString = formData.get("inputString")
    const hasMoreThanAscii = [...inputString].some(char => char.charCodeAt(0) > 127);
    console.log("hasMoreThanAscii: ", hasMoreThanAscii, inputString)
    if (hasMoreThanAscii) {
        DisplayError("Input string has non-ASCII characters!")
        return
    }
    var img = document.querySelector(`div[id="encode"] img`);
    console.log(img)
    const height = img.height;
    const width = img.width;
    if (inputString.length*8 > height*width) {
        DisplayError("Message is too long!")
        return
    }

    const fileNameArray = imgInput.value.split("\\")
    const fullFileName = fileNameArray[fileNameArray.length-1]
    formData.append("fileName", formData.get("imgFile").name)
    formData.delete("imgFile")
    console.log(...formData, fullFileName)
    try {
        const response = await fetch(`./encode`, {
            method: "POST",
            body: formData
        })

        if(!response.ok) throw new Error(response.statusText)
        console.log(response.statusText)
    } catch(err) {
        console.error(err)
    }
    const fileDownloadNameArray = fullFileName.split('.')
    const fileExtension = '.'+fileDownloadNameArray[1]
    const fileName = fileDownloadNameArray[0]
    if (fileName.includes('_steg')) {
        window.location.href = `./download?fileName=${fileName+fileExtension}`
        return
    }
    window.location.href = `./download?fileName=${fileName+'_steg'+fileExtension}`
}

async function DecodeHandler(e) {
    e.preventDefault()
    const imgInput = document.querySelector('div[id="decode"] input[type="file"]')
    const passwordInput = document.querySelector('div[id="decode"] #password')
    const fileNameArray = imgInput.value.split("\\")
    const fullFileName = fileNameArray[fileNameArray.length-1]
    console.log(fullFileName)
    try {
        const response = await fetch(`./decode?fileName=${fullFileName}&password=${passwordInput.value}`, {
            method: "POST",
        })
        console.log(response)
        const errorMessage = document.querySelector('#errorMessage')

        if(!response.ok) {
            errorMessage.innerHTML = response.statusText
            throw new Error(response.statusText)
        }
        const data = await response.json()
        const textInput = document.querySelector('div[id="decode"] #output')
        if (data.error) {
            errorMessage.innerHTML = data.error
        } else {
            textInput.value = data
            const outputDiv = document.querySelector(`div[id="outputDiv"]`)
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
            element.setAttribute('download', "output.txt");
            element.innerHTML = "Download output"
            outputDiv.appendChild(element);
        }
        console.log(textInput)
        console.log(response.statusText)


    } catch(err) {
        console.error(err)
    }
}

function DisplayHandler(id) {
    const encodeDiv = document.querySelector(`div[id="encode"]`)
    const decodeDiv = document.querySelector(`div[id="decode"]`)
    if (id == "encode") {
        encodeDiv.classList.remove("hidden")
        decodeDiv.classList.add("hidden")
    } else {
        encodeDiv.classList.add("hidden")
        decodeDiv.classList.remove("hidden")
    }
}

function DisplayError(msg) {
    const errorMessage = document.querySelector('#errorMessage')
    errorMessage.innerHTML = msg
    console.error(msg)
}

window.onload = (event) => {   
    console.log("page is fully loaded");
    const encodeInput = document.querySelector('div[id="encode"] input[type="file"]')
    const decodeInput = document.querySelector('div[id="decode"] input[type="file"]')
    const encodeForm = document.querySelector('div[id="encode"] #img-form')
    const decodeForm = document.querySelector('div[id="decode"] #img-form')
    const displayButtons = document.getElementsByClassName('display')
    console.log(encodeInput.id)
    encodeInput.id = "encode"
    decodeInput.id = "decode"
    encodeInput.addEventListener('change', UploadHandler)
    decodeInput.addEventListener('change', UploadHandler)
    encodeForm.addEventListener('submit', EncodeHandler)
    decodeForm.addEventListener('submit', DecodeHandler)
    for(let button of displayButtons) {
        button.addEventListener('click', () => DisplayHandler(button.id))
    };
    // const form = document.getElementById("form");
    // form.addEventListener("submit", logSubmit);
}

