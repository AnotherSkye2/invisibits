import { UploadHandler } from "./methods/UploadHandler";
import { EncodeHandler } from "./methods/EncodeHandler";
import { DecodeHandler } from "./methods/DecodeHandler";

window.onload = () => {   
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
}

