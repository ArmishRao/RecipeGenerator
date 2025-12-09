// // // FIXED script.js
// const uploadBtn = document.getElementById("uploadBtn"); // REMOVED COMMENT
// const imageUpload = document.getElementById("imageUpload");
// const fileName = document.getElementById("fileName");
// const modal = document.getElementById("modal");
// const modalImg = document.getElementById("modalImg");
// const closeModal = document.getElementById("closeModal");
// const scanBtn = document.getElementById("scanBtn");
// const scanMsg = document.getElementById("scanMsg");
// const ingredientsDiv = document.getElementById("ingredients");
// let uploadedFilename = "";

// // 1. Upload button functionality
// uploadBtn.addEventListener('click', function() {
//     imageUpload.click();
// });

// imageUpload.addEventListener('change', function() {
//     if (this.files && this.files[0]) {
//         const file = this.files[0];
//         fileName.textContent = `Uploaded: ${file.name}`;
//         uploadedFilename = file.name;

//         // Make filename clickable to preview
//         fileName.style.cursor = 'pointer';
//         fileName.style.color = 'blue';
//         fileName.style.textDecoration = 'underline';

//         // Preview image when filename is clicked
//         fileName.onclick = function() {
//             const reader = new FileReader();
//             reader.onload = function(e) {
//                 modal.style.display = "flex";
//                 modalImg.src = e.target.result;
//             };
//             reader.readAsDataURL(file);
//         };

//         // Close modal functionality
//         closeModal.onclick = function() {
//             modal.style.display = "none";
//         };

//         modal.onclick = function(e) {
//             if (e.target == modal) {
//                 modal.style.display = "none";
//             }
//         };

//         // Upload to server
//         const formData = new FormData();
//         formData.append("image", file);

//         fetch("/upload_image", {
//             method: "POST",
//             body: formData
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log("Server response:", data);
//             scanMsg.textContent = "Image uploaded successfully! Click Scan to detect ingredients.";
//             scanMsg.style.color = "green";
//         })
//         .catch(error => {
//             console.error("Error:", error);
//             scanMsg.textContent = "Upload failed! Please try again.";
//             scanMsg.style.color = "red";
//         });
//     }
// });

// // 2. Scan button functionality - fixed version
// scanBtn.addEventListener("click", function() {
//     if (!uploadedFilename) {
//         scanMsg.textContent = "Please upload an image first!";
//         scanMsg.style.color = "red";
//         return;
//     }

//     scanMsg.textContent = "Scanning image for ingredients...";
//     scanMsg.style.color = "blue";

//     const formData = new FormData();
//     formData.append('text', uploadedFilename);

//     fetch('/predict', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log("Detection Response:", data);
        
//         // Clear previous results
//         ingredientsDiv.innerHTML = "";
        
//         if (data.items && data.items.length > 0) {
//             // Display detected ingredients
//             const title = document.createElement('h3');
//             title.textContent = "Detected Ingredients:";
//             ingredientsDiv.appendChild(title);
            
//             data.items.forEach(ingredient => {
//                 const p = document.createElement('p');
//                 p.textContent = `• ${ingredient}`;
//                 ingredientsDiv.appendChild(p);
//             });
            
//             // Add button to generate recipe from detected ingredients
//             const recipeBtn = document.createElement('button');
//             recipeBtn.textContent = "Generate Recipe from These Ingredients";
//             recipeBtn.style.marginTop = "10px";
//             recipeBtn.style.padding = "10px";
//             recipeBtn.style.backgroundColor = "#8FAD88";
//             recipeBtn.style.color = "white";
//             recipeBtn.style.border = "none";
//             recipeBtn.style.cursor = "pointer";
            
//             recipeBtn.addEventListener('click', function() {
//                 // Redirect to recipe page with ingredients
//                 const ingredientsString = data.items.join(", ");
//                 window.location.href = `/generaterecipe?ingredients=${encodeURIComponent(ingredientsString)}`;
//             });
            
//             ingredientsDiv.appendChild(recipeBtn);
            
//             scanMsg.textContent = `Found ${data.items.length} ingredients!`;
//             scanMsg.style.color = "green";
//         } else {
//             scanMsg.textContent = "No ingredients detected in the image.";
//             scanMsg.style.color = "orange";
//         }
//     })
//     .catch(error => {
//         console.error("Error:", error);
//         scanMsg.textContent = "Scan failed! Please try again.";
//         scanMsg.style.color = "red";
//     });
// });
// // In the scanBtn event listener, replace the fetch call:
// fetch('/detect_and_generate', {
//     method: 'POST',
//     body: formData
// })
// .then(response => response.json())
// .then(data => {
//     console.log("Detection Response:", data);
    
//     // Clear previous results
//     ingredientsDiv.innerHTML = "";
    
//     if (data.detected_items && data.detected_items.length > 0) {
//         // Display detected ingredients
//         const title = document.createElement('h3');
//         title.textContent = "Detected Ingredients:";
//         ingredientsDiv.appendChild(title);
        
//         data.detected_items.forEach(ingredient => {
//             const p = document.createElement('p');
//             p.textContent = `• ${ingredient}`;
//             ingredientsDiv.appendChild(p);
//         });
        
//         // Display generated recipe
//         const recipeTitle = document.createElement('h3');
//         recipeTitle.textContent = "Generated Recipe:";
//         recipeTitle.style.marginTop = "20px";
//         ingredientsDiv.appendChild(recipeTitle);
        
//         const recipeDiv = document.createElement('div');
//         recipeDiv.textContent = data.recipe;
//         recipeDiv.style.whiteSpace = "pre-wrap";
//         recipeDiv.style.padding = "10px";
//         recipeDiv.style.backgroundColor = "#f8f9fa";
//         recipeDiv.style.borderRadius = "5px";
//         ingredientsDiv.appendChild(recipeDiv);
        
//         scanMsg.textContent = `Found ${data.detected_items.length} ingredients and generated recipe!`;
//         scanMsg.style.color = "green";
//     } else {
//         scanMsg.textContent = "No ingredients detected in the image.";
//         scanMsg.style.color = "orange";
//     }
// })// Add this function to create and handle PDF download
// function generatePDF(recipeTitle, ingredients, recipeText) {
//     // Show loading message
//     scanMsg.textContent = "Generating PDF...";
//     scanMsg.style.color = "blue";
    
//     // Prepare data for PDF generation
//     const pdfData = {
//         title: recipeTitle || "Generated Recipe",
//         ingredients: Array.isArray(ingredients) ? ingredients : ingredients.split(', '),
//         recipe: recipeText
//     };
    
//     // Call the PDF generation endpoint
//     fetch('/generate_pdf_simple', {  // You can use '/generate_pdf' for more advanced formatting
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(pdfData)
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success && data.pdf_base64) {
//             // Create download link
//             const link = document.createElement('a');
//             link.href = 'data:application/pdf;base64,' + data.pdf_base64;
//             link.download = data.filename || 'recipe.pdf';
            
//             // Trigger download
//             document.body.appendChild(link);
//             link.click();
//             document.body.removeChild(link);
            
//             scanMsg.textContent = "PDF downloaded successfully!";
//             scanMsg.style.color = "green";
//         } else {
//             throw new Error(data.error || 'Failed to generate PDF');
//         }
//     })
//     .catch(error => {
//         console.error("PDF generation error:", error);
//         scanMsg.textContent = "Failed to generate PDF: " + error.message;
//         scanMsg.style.color = "red";
//     });
// }

// // Also, add this function to create PDF button
// function createPDFButton(ingredients, recipeText) {
//     const pdfBtn = document.createElement('button');
//     pdfBtn.textContent = "Save Recipe as PDF";
//     pdfBtn.style.marginTop = "10px";
//     pdfBtn.style.marginLeft = "10px";
//     pdfBtn.style.padding = "10px 15px";
//     pdfBtn.style.backgroundColor = "#2E8B57";  // Green color
//     pdfBtn.style.color = "white";
//     pdfBtn.style.border = "none";
//     pdfBtn.style.borderRadius = "5px";
//     pdfBtn.style.cursor = "pointer";
//     pdfBtn.style.fontSize = "14px";
    
//     pdfBtn.addEventListener('click', function() {
//         // You can extract the recipe title from the recipe text or use a default
//         const recipeLines = recipeText.split('\n');
//         const recipeTitle = recipeLines[0] || "Generated Recipe";
        
//         generatePDF(recipeTitle, ingredients, recipeText);
//     });
    
//     return pdfBtn;
// // }

// Enhanced JavaScript with better UX
const uploadBtn = document.getElementById("uploadBtn");
const imageUpload = document.getElementById("imageUpload");
const fileName = document.getElementById("fileName");
const modal = document.getElementById("modal");
const modalImg = document.getElementById("modalImg");
const closeModal = document.getElementById("closeModal");
const scanBtn = document.getElementById("scanBtn");
const scanMsg = document.getElementById("scanMsg");
const ingredientsDiv = document.getElementById("ingredients");

let uploadedFilename = "";
let currentFile = null; // <-- NEW: Track current file

// 1. Enhanced upload button functionality
uploadBtn.addEventListener('click', function() {

    imageUpload.click();
});

imageUpload.addEventListener('change', async function() {
    if (this.files && this.files[0]) {
        const file = this.files[0];
        currentFile = file; // <-- Store the current file
        uploadedFilename = file.name;
        
        // Validate file type
        if (!file.type.match('image.*')) {
            showMessage("Please upload an image file (JPEG, PNG, etc.)", "error");
            return;
        }
        
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showMessage("File size should be less than 5MB", "error");
            return;
        }
        
        fileName.innerHTML = `
            <i class="fas fa-image"></i> 
            Uploaded: <strong>${file.name}</strong> 
            <span style="color: #666; font-size: 14px;">(${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
        `;

        // Make filename clickable with better styling
        fileName.style.cursor = 'pointer';
        fileName.style.color = '#2E8B57';
        fileName.style.padding = '12px 20px';
        fileName.style.background = '#f8f9fa';
        fileName.style.borderRadius = '10px';
        fileName.style.display = 'inline-block';
        fileName.style.marginTop = '10px';
        fileName.style.border = '2px dashed #8FAD88';

        // Preview image when filename is clicked
        fileName.onclick = function() {
            const reader = new FileReader();
            reader.onload = function(e) {
                modal.style.display = "flex";
                modalImg.src = e.target.result;
            };
            reader.readAsDataURL(file);
        };

        // Close modal functionality
        closeModal.onclick = function() {
            modal.style.display = "none";
        };

        modal.onclick = function(e) {
            if (e.target == modal) {
                modal.style.display = "none";
            }
        };

        // Show loading for upload
        showMessage("Uploading image...", "info");
        
        // Upload to server (optional - for saving to server)
        const formData = new FormData();
        formData.append("image", file);

        try {
            const response = await fetch("/upload_image", {
                method: "POST",
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Upload failed');
            }
            
            const data = await response.json();
            console.log("Server response:", data);
            showMessage("✓ Image uploaded successfully! Click 'Scan Image' to detect ingredients.", "success");
            
            // Enable scan button with animation
            scanBtn.style.animation = "pulse 2s infinite";
            scanBtn.innerHTML = '<i class="fas fa-search"></i> Scan Image';
            
        } catch (error) {
            console.error("Error:", error);
            showMessage("✗ Upload failed! Please try again.", "error");
        }

    }
});

// 2. Enhanced scan button functionality - UPDATED with direct file upload
scanBtn.addEventListener("click", async function() {
    if (!currentFile) { // <-- Check if we have a current file
        showMessage("Please upload an image first!", "warning");
        return;
    }

    // Show loading state
    scanBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning...';
    scanBtn.disabled = true;
    showMessage("🔍 Scanning image for ingredients...", "info");

    // Send the file directly instead of just filename
    const formData = new FormData();
    formData.append('image', currentFile); // <-- Send the actual file

    try {
        // Try direct_predict endpoint first (new endpoint)
        let response = await fetch('/direct_predict', {
            method: 'POST',
            body: formData
        });
        
        // If direct_predict doesn't exist, fall back to predict
        if (response.status === 404) {
            console.log("direct_predict endpoint not found, falling back to predict");
            
            // Try with filename for backward compatibility
            const fallbackFormData = new FormData();
            fallbackFormData.append('text', uploadedFilename);
            
            response = await fetch('/predict', {
                method: 'POST',
                body: fallbackFormData
            });
        }
        
        if (!response.ok) {
            throw new Error('Scan failed');
        }
        
        const data = await response.json();
        console.log("Detection Response:", data);
        
        // Reset scan button
        scanBtn.innerHTML = '<i class="fas fa-search"></i> Scan Image';
        scanBtn.disabled = false;
        scanBtn.style.animation = "none";
        
        // Handle error response
        if (data.error) {
            showMessage(`✗ ${data.error}`, "error");
            if (data.suggestion) {
                showMessage(data.suggestion, "info");
            }
            return;
        }
        
        // Clear previous results
        ingredientsDiv.innerHTML = "";
        
        if (data.items && data.items.length > 0) {
            // Create ingredients card
            const card = document.createElement('div');
            card.className = 'ingredients-card';
            card.style.animation = "fadeIn 0.5s ease-out";
            
            // Display detected ingredients
            const title = document.createElement('h3');
            title.innerHTML = '<i class="fas fa-clipboard-list"></i> Detected Ingredients:';
            card.appendChild(title);
            
            const list = document.createElement('div');
            list.className = 'ingredients-list';
            
            data.items.forEach(ingredient => {
                const item = document.createElement('div');
                item.className = 'ingredient-item';
                item.innerHTML = `
                    <span class="ingredient-icon">🥬</span>
                    <span class="ingredient-name">${ingredient}</span>
                `;
                list.appendChild(item);
            });
            card.appendChild(list);
            
            // Show recipe if generated
            if (data.recipe && data.recipe !== "No ingredients detected.") {
                const recipeTitle = document.createElement('h4');
                recipeTitle.innerHTML = '<i class="fas fa-utensils"></i> Suggested Recipe:';
                recipeTitle.style.marginTop = "20px";
                card.appendChild(recipeTitle);
                
                const recipeDiv = document.createElement('div');
                recipeDiv.className = 'recipe-preview';
                recipeDiv.textContent = data.recipe.length > 150 ? 
                    data.recipe.substring(0, 150) + "..." : data.recipe;
                card.appendChild(recipeDiv);
                
                // Action buttons
                const buttonsDiv = document.createElement('div');
                buttonsDiv.className = 'action-buttons';
                buttonsDiv.style.marginTop = "20px";
                buttonsDiv.style.display = "flex";
                buttonsDiv.style.gap = "10px";
                buttonsDiv.style.flexWrap = "wrap";
                
                // View full recipe button
                const viewRecipeBtn = document.createElement('button');
                viewRecipeBtn.innerHTML = '<i class="fas fa-book-open"></i> View Full Recipe';
                viewRecipeBtn.className = 'action-btn';
                viewRecipeBtn.style.backgroundColor = "#2E8B57";
                
                viewRecipeBtn.addEventListener('click', function() {
                    const ingredientsString = data.items.join(", ");
                    window.location.href = `/generaterecipe?ingredients=${encodeURIComponent(ingredientsString)}`;
                });
                
                // Generate new recipe button
                const generateBtn = document.createElement('button');
                generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate New Recipe';
                generateBtn.className = 'action-btn';
                generateBtn.style.backgroundColor = "#8FAD88";
                
                generateBtn.addEventListener('click', function() {
                    window.location.href = `/generaterecipe?ingredients=${encodeURIComponent(data.ingredients_used || data.items.join(", "))}`;
                });
                
                buttonsDiv.appendChild(viewRecipeBtn);
                buttonsDiv.appendChild(generateBtn);
                card.appendChild(buttonsDiv);
            } else {
                // Generate recipe button only
                const recipeBtn = document.createElement('button');
                recipeBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Recipe';
                recipeBtn.className = 'action-btn';
                recipeBtn.style.marginTop = "20px";
                recipeBtn.style.width = "100%";
                
                recipeBtn.addEventListener('click', function() {
                    const ingredientsString = data.items.join(", ");
                    window.location.href = `/generaterecipe?ingredients=${encodeURIComponent(ingredientsString)}`;
                });
                
                card.appendChild(recipeBtn);
            }
            
            ingredientsDiv.appendChild(card);
            showMessage(`✓ Found ${data.items.length} ingredients!`, "success");
            
            // Smooth scroll to results
            ingredientsDiv.scrollIntoView({ behavior: 'smooth' });
            
        } else {
            showMessage("No ingredients detected in the image. Try a clearer picture.", "warning");
        }
        
    } catch (error) {
        console.error("Error:", error);
        scanBtn.innerHTML = '<i class="fas fa-search"></i> Scan Image';
        scanBtn.disabled = false;
        showMessage("✗ Scan failed! Please try again.", "error");
    }
});

// Helper function to show messages
function showMessage(text, type = "info") {
    const colors = {
        success: { bg: "#d4edda", text: "#155724", border: "#c3e6cb" },
        error: { bg: "#f8d7da", text: "#721c24", border: "#f5c6cb" },
        warning: { bg: "#fff3cd", text: "#856404", border: "#ffeaa7" },
        info: { bg: "#d1ecf1", text: "#0c5460", border: "#bee5eb" }
    };
    
    scanMsg.innerHTML = text;
    scanMsg.style.backgroundColor = colors[type].bg;
    scanMsg.style.color = colors[type].text;
    scanMsg.style.border = `2px solid ${colors[type].border}`;
    scanMsg.style.padding = "12px 20px";
    scanMsg.style.borderRadius = "10px";
    scanMsg.style.marginTop = "15px";
    scanMsg.style.display = "block";
    scanMsg.style.maxWidth = "800px";
    scanMsg.style.marginLeft = "auto";
    scanMsg.style.marginRight = "auto";
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .ingredients-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        max-width: 800px;
    }
    
    .ingredients-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
        margin-top: 15px;
    }
    
    .ingredient-item {
        padding: 12px 15px;
        background: #f8f9fa;
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-left: 4px solid #8FAD88;
    }
    
    .ingredient-icon {
        font-size: 20px;
    }
    
    .ingredient-name {
        font-weight: 500;
    }
    
    .recipe-preview {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        font-style: italic;
        line-height: 1.5;
        border-left: 4px solid #2E8B57;
    }
    
    .action-btn {
        padding: 12px 25px;
        border: none;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// Test function for debugging
function testImageAPI() {
    const testIngredients = ['apple', 'banana', 'orange'];
    const testRecipe = "Apple Banana Smoothie: A refreshing fruit smoothie perfect for breakfast.";
    
    console.log('=== TESTING IMAGE API ===');
    fetchRecipeImage(testIngredients.join(', '), testRecipe);
}

// Helper function for recipe page image fetching
function fetchRecipeImage(ingredients, recipeText) {
    // This function is for the recipe page, not needed here
    console.log('Recipe image fetch called');
}
