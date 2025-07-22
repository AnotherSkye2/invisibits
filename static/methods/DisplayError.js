export function DisplayError(msg) {
    const errorMessage = document.querySelector('#errorMessage')
    errorMessage.innerHTML = msg
    console.error(msg)
}