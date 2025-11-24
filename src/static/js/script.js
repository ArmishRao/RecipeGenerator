const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');

fileInput.addEventListener('change', function(event) {
    const [file] = event.target.files;
    if (file) {
        preview.src = URL.createObjectURL(file);
    } else {
        preview.src = '#';
    }
});

// Optional: prevent form submission for demo
const form = document.getElementById('upload-form');
form.addEventListener('submit', function(e) {
    e.preventDefault();
    alert("Form submitted! (In real app, this would go to backend)");
});
