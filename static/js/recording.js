// Get the video element
const video = document.getElementById("video");

// Get the start and stop buttons
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

// Variables to store the media stream and recorded chunks
let mediaStream = null;
let chunks = [];

// Start recording function
function startRecording() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            // Set the media stream to the video element source
            video.srcObject = stream;
            mediaStream = stream;

            // Create a new MediaRecorder instance
            const mediaRecorder = new MediaRecorder(stream);

            // Start recording and store the recorded chunks
            mediaRecorder.start();
            chunks = [];

            // Push each recorded data chunk to the chunks array
            mediaRecorder.addEventListener("dataavailable", (event) => {
                chunks.push(event.data);
            });

            // Stop recording and save the recorded video file
            stopBtn.addEventListener("click", () => {
                mediaRecorder.stop();
                mediaStream.getTracks().forEach((track) => track.stop());
                saveRecording();
            });
        })
        .catch((error) => {
            console.error("Error accessing camera:", error);
        });
}

// Save the recorded video as a blob
function saveRecording() {
    const blob = new Blob(chunks, { type: "video/webm" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "recording.webm";
    a.click();
    URL.revokeObjectURL(url);
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
});
