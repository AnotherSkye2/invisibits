export function DisplayHandler(id) {
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