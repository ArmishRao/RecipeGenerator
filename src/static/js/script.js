const uploadBtn=document.getElementById("uploadBtn")
const imageUpload= document.getElementById("imageUpload")
const fileName= document.getElementById("fileName")
const modal = document.getElementById("modal");
const modalImg = document.getElementById("modalImg");
const closeModal = document.getElementById("closeModal");
const scanBtn = document.getElementById("scanBtn");
const scanMsg = document.getElementById("scanMsg");
let uploadedFilename= "";


uploadBtn.addEventListener('click', function() {
    imageUpload.click()
});
 
imageUpload.addEventListener('change', function() {
    if(this.files && this.files[0]) //ensures the user actually picked a file, allows array of files or js 1
    {
        const file = this.files[0];
        fileName.textContent = file.name;
        uploadedFilename=file.name;

        fileName.style.cursor = 'pointer';
        fileName.onclick = function()  {
        const reader = new FileReader();
        reader.onload = function(e) {
            modal.style.display = "flex"; // use flex to center
            modalImg.src = e.target.result;//target-filereader, result-the URL
            }//onload only triggers after the entire file has been read successfully.
        reader.readAsDataURL(file);//this reads the file and triggers onload
        }

        closeModal.onclick = function() {
            modal.style.display = "none";
        }

        modal.onclick = function(e) {
            if(e.target == modal) {
                modal.style.display = "none";
            }
        }

        const formData= new FormData();
        formData.append("image", file)

        fetch("/upload_image", {method:"POST", body: formData})//built-in JavaScript function that allows you to make HTTP requests    
        .then(response => response.json())
        .then(data => {
        console.log("Server response:", data);
        })
        .catch(error => console.error("Error:", error));
    }
});

// scanBtn.addEventListener('click', function() {
//     const fileURL= `/uploads/${uploadedFilename}`;
//     fetch(fileURL)
//     .then(response => response.blob())
//     .then(blob =>  {
//         const file = new File([blob], uploadedFilename, {type: blob.type});

//         const formData=new FormData()
//         formData.append('image', file)
//         fetch('/predict', {method: "POST", body: formData})
//         .then(response => response.json())
//         .then(data => {
//             console.log("Server Response: ", data);
//         })
//         .catch(error => console.error("Error:", error));
//     })
    

// })

scanBtn.addEventListener("click", function() {
    const formData= new FormData();
    formData.append('text', uploadedFilename)

    fetch('/predict', {
        method: 'POST', 
        body: formData
    })
    .then(response=> response.json())
    .then(data =>   console.log("Server says: ", data))
    .catch(error => console.error("Error:", error));
})
