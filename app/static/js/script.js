let video = document.getElementById("camera");
let canvas = document.createElement("canvas");
let context = canvas.getContext("2d");
let maskImg = document.getElementById("mask-img");
let resultDiv = document.getElementById("result");

// Start camera and stream video to the video element
async function startCamera() {
    try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("Camera not supported on this browser.");
            return;
        }

        let stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.onloadedmetadata = () => video.play();
    } catch (error) {
        console.error("Error accessing the camera: ", error);
        alert("Unable to access the camera. Please check camera permissions.");
    }
}

// Capture image from video stream and send for processing
async function captureImage() {
    if (video.readyState !== 4) {
        alert("Camera is not ready yet. Please wait.");
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        let formData = new FormData();
        formData.append("file", blob, "captured_image.jpg");

        try {
            let response = await fetch("/detect/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to process the image.");
            }

            let result = await response.json();
            if (result.mask_url) {
                updateMask(result.mask_url);
            } else {
                alert("Failed to generate mask.");
            }
        } catch (error) {
            console.error("Error processing image:", error);
            alert("Error processing image. Please try again.");
        }
    }, "image/jpeg");
}

// Update the mask dynamically
function updateMask(maskUrl) {
    // Append a unique query parameter to the URL to prevent caching
    const uniqueUrl = `${maskUrl}?t=${new Date().getTime()}`;

    // Clear the previous mask
    maskImg.src = ""; // Clear the src to force reload
    resultDiv.style.display = "none"; // Hide the result section while loading

    // Set the new mask URL with the unique query parameter
    maskImg.src = uniqueUrl;

    // Show the result section once the image is loaded
    maskImg.onload = () => {
        resultDiv.style.display = "block";
    };
}

// Add event listener for the capture button
document.getElementById("capture-btn").addEventListener("click", async () => {
    await captureImage();
});

// Add event listener for file upload
document.getElementById("upload-btn").addEventListener("click", async () => {
    let fileInput = document.getElementById("upload-input");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    try {
        let response = await fetch("/detect/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to process the image.");
        }

        let result = await response.json();
        if (result.mask_url) {
            updateMask(result.mask_url);
        } else {
            alert("Failed to generate mask.");
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        alert("Error uploading file. Please try again.");
    }
});

// Start camera on page load
window.onload = async () => {
    await startCamera();
};