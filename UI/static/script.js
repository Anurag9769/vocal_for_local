
let audioContext;
let recorder;

document.getElementById("recordButton").onclick = async () => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const input = audioContext.createMediaStreamSource(stream);
    recorder = new Recorder(input, { numChannels: 1 });

    recorder.record();
    document.getElementById("status").textContent = "Recording...";
    document.getElementById("recordButton").disabled = true;
    document.getElementById("stopButton").disabled = false;
 };

document.getElementById("stopButton").onclick = () => {
    recorder.stop();
    audioContext.close();

    recorder.exportWAV(blob => {
        /*const downloadLink = document.getElementById("downloadButton");
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'output.wav';
        downloadLink.textContent = 'Download Audio';
        downloadLink.style.display = 'inline';*/

        // Prepare for upload
        const formData = new FormData();
        formData.append('file', blob, 'output.wav');

        // Upload the audio
        fetch('/process-audio', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            //const response = await fetch("/process-audio", {
            //    method: "POST"
            //});
            //document.getElementById("status").textContent = data;
            document.getElementById("status").textContent = "";
            displayMessage(data['question'], 'user-message');
            displayMessage(data['answer'], 'bot-message');
        })
        .catch(error => {
            document.getElementById("status").textContent = "Upload failed.";
        });
        document.getElementById("status").textContent = "Recording stopped. Processing audio...";
        document.getElementById("recordButton").disabled = false;
        document.getElementById("stopButton").disabled = true;
    });
};

document.getElementById('send-btn').addEventListener('click', function() {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value;
    if (userMessage.trim() === '') return;

     fetch('/process-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userMessage }) // Use JSON.stringify to properly format the JSON
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data['answer'], 'bot-message');
        })
        .catch(error => {
            document.getElementById("status").textContent = "processing failed.";
        });

    // Display user message
    displayMessage(userMessage, 'user-message');

    // Simulate bot response
    //setTimeout(() => {
    //    const botResponse = "You said: " + userMessage; // Placeholder for bot response
    //    displayMessage(botResponse, 'bot-message');
    //}, 1000);

    inputField.value = ''; // Clear input field
});

function displayMessage(message, type) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}`;
    messageElement.textContent = message;

    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}
