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

// scanBtn.addEventListener("click", function() {
//     const formData= new FormData();
//     formData.append('text', uploadedFilename)

//     fetch('/predict', {
//         method: 'POST', 
//         body: formData
//     })
//     .then(response=> response.json())
//     .then(data =>   {
//         const list=data.items;
//         const ingredients=document.getElementById("ingredients")
//         ingredients.innerHTML="" //.innerHTML is a property that represents the HTML inside an element.
//         list.forEach(ingredient => {
//             const p=document.createElement('p')
//             p.textContent=ingredient
//             ingredients.appendChild(p)//.appendChild() adds the element as a child of the container.
//         })
//     })
//     .catch(error => console.error("Error:", error));
// }// Scan button click - UPDATED VERSION
scanBtn.addEventListener("click", function() {
    if (!uploadedFilename) {
        alert("Please upload an image first!");
        return;
    }
    
    // Show loading
    scanBtn.disabled = true;
    const originalText = scanBtn.textContent;
    scanBtn.textContent = "Processing...";
    
    const formData = new FormData();
    formData.append('text', uploadedFilename);
    
    console.log("Sending prediction request for:", uploadedFilename);
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log("Response status:", response.status, response.statusText);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data);
        
        // Reset button
        scanBtn.disabled = false;
        scanBtn.textContent = originalText;
        
        // Display results
        if (data.success === false) {
            displayError(data.error || "Unknown error");
        } else {
            displayResults(data);
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        
        // Reset button
        scanBtn.disabled = false;
        scanBtn.textContent = originalText;
        
        displayError(error.message);
    });
});

// Display results function - UPDATED
function displayResults(data) {
    const container = document.getElementById("ingredients");
    container.innerHTML = "";
    
    console.log("Displaying data:", data);
    
    // Display detected ingredients
    const ingredientsTitle = document.createElement('h3');
    ingredientsTitle.textContent = " Detected Ingredients:";
    container.appendChild(ingredientsTitle);
    
    // Check if items exist and is an array
    if (data.items && Array.isArray(data.items) && data.items.length > 0) {
        data.items.forEach(ingredient => {
            const p = document.createElement('p');
            p.textContent = `✓ ${ingredient}`;
            p.style.padding = "5px 0";
            p.style.borderBottom = "1px solid #eee";
            container.appendChild(p);
        });
        
        // Show count
        const countP = document.createElement('p');
        countP.textContent = `Total: ${data.items.length} items detected`;
        countP.style.fontStyle = "italic";
        countP.style.marginTop = "10px";
        container.appendChild(countP);
    } else {
        const p = document.createElement('p');
        p.textContent = "⚠ No specific ingredients detected";
        p.style.color = "#ff6b6b";
        container.appendChild(p);
    }
    
    // Display generated recipe
    const recipeTitle = document.createElement('h3');
    recipeTitle.textContent = "📝 Generated Recipe:";
    recipeTitle.style.marginTop = "30px";
    recipeTitle.style.paddingTop = "20px";
    recipeTitle.style.borderTop = "2px solid #8FAD88";
    container.appendChild(recipeTitle);
    
    const recipeDiv = document.createElement('div');
    recipeDiv.className = "recipe-content";
    
    if (data.recipe && data.recipe.trim() !== "") {
        recipeDiv.textContent = data.recipe;
    } else {
        recipeDiv.textContent = "No recipe generated. Please try with a different image.";
        recipeDiv.style.color = "#ff6b6b";
    }
    
    container.appendChild(recipeDiv);
}

// Error display function
function displayError(errorMessage) {
    const container = document.getElementById("ingredients");
    container.innerHTML = "";
    
    const errorTitle = document.createElement('h3');
    errorTitle.textContent = " Error";
    errorTitle.style.color = "#ff6b6b";
    container.appendChild(errorTitle);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = "recipe-content";
    errorDiv.style.backgroundColor = "#ffe6e6";
    errorDiv.style.borderLeft = "4px solid #ff6b6b";
    errorDiv.textContent = `Error: ${errorMessage}\n\nPlease try again or upload a different image.`;
    container.appendChild(errorDiv);
}

// Also update the upload function to log better:
imageUpload.addEventListener('change', function() {
    if(this.files && this.files[0]) {
        const file = this.files[0];
        
        // Display file name
        fileName.textContent = `📄 ${file.name}`;
        uploadedFilename = file.name;
        
        // Enable scan button
        scanBtn.disabled = false;
        scanBtn.style.opacity = "1";
        
        // Create preview
        const reader = new FileReader();
        reader.onload = function(e) {
            fileName.style.cursor = 'pointer';
            fileName.title = "Click to preview";
            fileName.onclick = function() {
                modal.style.display = "flex";
                modalImg.src = e.target.result;
            };
        };
        reader.readAsDataURL(file);
        
        // Upload to server
        const formData = new FormData();
        formData.append("image", file);
        
        console.log("Uploading file:", file.name);
        
        fetch("/upload_image", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Upload response:", data);
            if (data.success) {
                fileName.textContent += " ";
                uploadedFilename = data.filename;
                console.log("Server filename:", uploadedFilename);
            } else {
                fileName.textContent += " ";
                console.error("Upload failed:", data.error);
            }
        })
        .catch(error => {
            console.error("Upload error:", error);
            fileName.textContent += " ❌";
        });
    }
});