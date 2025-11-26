const uploadBtn=document.getElementById("uploadBtn")
const imageUpload= document.getElementById("imageUpload")
const fileName= document.getElementById("fileName")
const modal = document.getElementById("modal");
const modalImg = document.getElementById("modalImg");
const closeModal = document.getElementById("closeModal");


uploadBtn.addEventListener('click', function() {
    imageUpload.click()
});
 
imageUpload.addEventListener('change', function() {
    if(this.files && this.files[0]) //ensures the user actually picked a file, allows array of files or js 1
    {
        const file = this.files[0];
        fileName.textContent = file.name;

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