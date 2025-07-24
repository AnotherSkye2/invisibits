import { DisplayError } from "./DisplayError.js"

export async function EncodeHandler(e) {
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