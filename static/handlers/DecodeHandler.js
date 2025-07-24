import { DisplayError } from "./DisplayError.js"

export async function DecodeHandler(e) {
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
        if(!response.ok) {
            DisplayError(response.statusText)
        }
        const data = await response.json()
        const textInput = document.querySelector('div[id="decode"] #output')
        if (data.error) {
            DisplayError(data.error)
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