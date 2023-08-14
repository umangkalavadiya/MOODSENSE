// Get the video element
const video = document.getElementById("video");

// Get the start and stop buttons
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

// Variables to store the media stream and recorded chunks
let mediaStream = null;
let mediaRecorder = null;
let recordedChunks = [];

// Start recording function
function startRecording() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            // Set the media stream to the video element source
            video.srcObject = stream;
            mediaStream = stream;

            // Create a new MediaRecorder instance
            mediaRecorder = new MediaRecorder(stream);
            // Start recording and store the recorded chunks
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            // Event listener for stop recording
            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: "video/mp4" });
                sendRecordingToDjango(blob); 
                // const url = URL.createObjectURL(blob);
                // const a = document.createElement("a");
                // a.href = url;
                // a.download = "recording.mp4";
                // a.click();
                // URL.revokeObjectURL(url);

                recordedChunks = []; // Clear recorded chunks
            };

            // Start recording
            mediaRecorder.start();
        })
        .catch((error) => {
            console.error("Error accessing camera:", error);
        });
}

// Stop recording function
function stopRecording() {
    mediaRecorder.stop();
    mediaStream.getTracks().forEach((track) => track.stop());
}

// Add click event listener to the start button
startBtn.addEventListener("click", () => {
    startBtn.disabled = true;
    stopBtn.disabled = false;
    startRecording();
});

// Add click event listener to the stop button
stopBtn.addEventListener("click", () => {
    startBtn.disabled = false;
    stopBtn.disabled = true;
    stopRecording();
});


// Function to send recorded video data to Django for saving
function sendRecordingToDjango(blob) {
    const formData = new FormData();
    formData.append("video_file", blob, "recording.mp4");

    // Send the recorded video data to Django using AJAX
    $.ajax({
        type: "POST",
        url: "/recording/", // Replace 'recording' with the name of the recording view in your URLs
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log("Recording saved successfully.");
            window.location.href = "/emotion_analysis/";
        },
        error: function(error) {
            console.error("Error saving recording:", error);
        },
    });
}


