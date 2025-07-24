import { DisplayError } from "./DisplayError.js";

export async function UploadHandler() {
    if (this.files && this.files[0]) {
        const img = document.querySelector(`div[id=${this.id}] img`);
        img.onload = () => {
            URL.revokeObjectURL(img.src);  // no longer needed, free memory
        }
        const maxSizeInMB = 5
        if(this.files[0].size / (1024 ** 2) > maxSizeInMB) {
            const imgInput = document.querySelector(`div[id=${this.id}] .imgInput`)
            DisplayError("File size is too big!")
            imgInput.value = ''
            return
        }
        
        img.src = URL.createObjectURL(this.files[0]);
        const imgForm = document.querySelector(`div[id=${this.id}] #img-form`)
        const formData = new FormData(imgForm)
        formData.append("fileName", formData.get("imgFile").name)
        formData.delete("inputString")
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
