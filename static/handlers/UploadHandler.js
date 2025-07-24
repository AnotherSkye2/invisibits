import { DisplayError } from "./DisplayError.js";

export async function UploadHandler() {
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
