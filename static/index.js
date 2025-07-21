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
    const imgInput = document.querySelector('div[id="encode"] input[type="file"]')
    const passwordInput = document.querySelector('div[id="encode"] #password')
    const textForm = document.querySelector('div[id="encode"] #text-form')
    const formData = new FormData(textForm)
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
    console.log(formData, fullFileName)
    try {
        const response = await fetch(`./encode?fileName=${fullFileName}&password=${passwordInput.value}`, {
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

        if(!response.ok) throw new Error(response.statusText)
        const data = await response.json()
        const textInput = document.querySelector('div[id="decode"] #output')
        const errorMessage = document.querySelector('#errorMessage')
        if (data.error) {
            errorMessage.innerHTML = data.error
        } else {
            textInput.value = data
        }
        console.log(data, typeof data)
        console.log(response.statusText)
        const decodeDiv = document.querySelector(`div[id="decode"]`)
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
        element.setAttribute('download', "output.txt");
        element.innerHTML = "Download output"

        decodeDiv.appendChild(element);
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

function DisplayError(msg) {
    const errorMessage = document.querySelector('#errorMessage')
    errorMessage.innerHTML = msg
    console.error(msg)
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

