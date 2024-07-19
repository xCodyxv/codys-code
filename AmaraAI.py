# This is made to work in google colab

# pip install
!pip install Flask pyngrok

# Set your ngrok authtoken (replace 'YOUR_NGROK_AUTH_TOKEN' with your actual token)
!ngrok authtoken YOUR_NGROK_AUTH_TOKEN

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Amara means guiding light

from flask import Flask, request, jsonify, render_template_string
from google.generativeai import GenerativeModel
import google.generativeai as genai
from google.colab import userdata
import os
from pyngrok import ngrok

# Setup your API key using the Colab userdata module
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Please set your API key in Colab.")

# Initialize the Gemini 1.5 model
model = GenerativeModel('gemini-1.5-flash')

# Create Flask app
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def ai_assistant():
    return render_template_string(html_content)

# Define a route for handling chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': 'Error: No message received.'})

    # Generate the response from the Gemini 1.5 model
    response = model.generate_content(user_message)
    return jsonify({'response': response.text})

# HTML content for the Amara AI assistant page
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amara AI Assistant</title>
    <style>
        body, html {
            font-family: 'Rajdhani', sans-serif;
            color: #00ffff;
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            background-image: url('https://i.postimg.cc/sfbKnVsv/cyberpunkmoon-ezgif-com-reverse.gif');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .main-container {
            display: grid;
            grid-template-columns: 250px 1fr 250px;
            grid-template-rows: auto 1fr auto;
            gap: 20px;
            height: 100vh;
            padding: 20px;
            box-sizing: border-box;
            background: rgba(0, 0, 0, 0.4);
        }
        .command-reminder, .container, #clock, .memory {
            background: rgba(30, 30, 50, 0.4);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(173, 216, 230, 0.5);
        }
        .command-reminder {
            grid-column: 1;
            grid-row: 1 / span 3;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .container {
            grid-column: 2;
            grid-row: 1 / span 3;
            display: flex;
            flex-direction: column;
        }
        .side-panel {
            grid-column: 3;
            grid-row: 1 / span 3;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        h1, h2, h3 { color: yellow; margin-top: 0; text-shadow: 0 0 10px #ffffff; }
        #voice-indicator-container {
            width: 220px;
            height: 80px;
            margin: 20px auto;
            border: 2px solid rgba(173, 216, 230, 0.3);
            border-radius: 10px;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(30, 30, 50, 0.4);
            box-shadow: 0 0 15px rgba(173, 216, 230, 0.2);
        }
        #voice-indicator {
            width: 200px;
            height: 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .voice-line {
            width: 4px;
            height: 20px;
            background-color: #00ffff;
            border-radius: 2px;
            transition: height 0.1s ease;
        }
        @keyframes voicePulse {
            0% { height: 10px; }
            50% { height: 50px; }
            100% { height: 10px; }
        }
        .listening .voice-line {
            animation: voicePulse 0.5s infinite;
            animation-delay: calc(var(--i) * 0.1s);
        }
        #status, #info, #chat-window, #update-box {
            margin-top: 20px;
            font-size: 18px;
        }
        #chat-window {
            flex-grow: 1;
            overflow-y: auto;
            background: rgba(15, 52, 96, 0.3);
            border-radius: 10px;
            padding: 20px;
            text-align: left;
            margin: 20px 0;
        }
        .user-message { color: #ffffff; text-shadow: 0 0 5px #ffffff; }
        .ai-message { color: #00ffff; text-shadow: 0 0 5px #add8e6; }
        #update-box {
            background: rgba(173, 216, 230, 0.2);
            border: 2px solid #add8e6;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            color: #00ffff;
            text-shadow: 0 0 5px #add8e6;
        }
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: rgba(26, 26, 46, 0.4); }
        ::-webkit-scrollbar-thumb { background: #add8e6; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #00ffff; }
        #clock {
            font-size: 24px;
            text-align: center;
            color: yellow;
            text-shadow: 0 0 10px #ffffff;
        }
        #command-box h3, #reminder-box h3, .memory h3 {
            margin-top: 0;
            border-bottom: 1px solid #add8e6;
            padding-bottom: 10px;
            cursor: pointer;
            user-select: none;
        }
        #command-box ul, #reminder-box ul, .memory ul {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 0;
            overflow: hidden;
            max-height: 500px;
            transition: max-height 0.5s ease-in-out;
        }
        #command-box li { margin-bottom: 10px; }
        #reminder-box { margin-top: 20px; }
        #reminder-list {
            max-height: 150px;
            overflow-y: auto;
        }
        .reminder-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }
        .reminder-item button {
            background: #add8e6;
            color: #1a1a2e;
            border: none;
            border-radius: 5px;
            padding: 2px 5px;
            cursor: pointer;
        }
        .collapsible-inactive {
            max-height: 0 !important;
            transition: max-height 0.5s ease-out !important;
        }
    </style>
</head>
<body>
<div class="main-container">
    <div class="command-reminder">
        <div id="command-box">
            <h3 onclick="toggleCollapsible('command-list')">Commands ▲</h3>
            <ul id="command-list">
                <li>"Hey Amara" - Jack in / Resume listening</li>
                <li>"pause" - Go offline</li>
                <li>"remember [info]" - Add to memory bank</li>
                <li>"update [change]" - Mod the interface</li>
                <li>"remind me to [task] at [time]" - Add a reminder</li>
            </ul>
        </div>
        <div id="reminder-box">
            <h3 onclick="toggleCollapsible('reminder-list')">Reminders ▲</h3>
            <ul id="reminder-list">
                <!-- Reminders will be dynamically added here -->
            </ul>
        </div>
    </div>
    <div class="container">
        <h1>Amara</h1>
        <p>Your friendly AI assistant, powered by Gemini 1.5. Here to help with a human touch.</p>
        <div id="voice-indicator-container">
            <div id="voice-indicator" class="listening">
                <div class="voice-line" style="--i: 0;"></div>
                <div class="voice-line" style="--i: 1;"></div>
                <div class="voice-line" style="--i: 2;"></div>
                <div class="voice-line" style="--i: 3;"></div>
                <div class="voice-line" style="--i: 4;"></div>
                <div class="voice-line" style="--i: 5;"></div>
                <div class="voice-line" style="--i: 6;"></div>
                <div class="voice-line" style="--i: 7;"></div>
            </div>
        </div>
        <div id="status">Status: Ready</div>
        <div id="info">Hey User! What's on your name?</div>
        <div id="chat-window">
            <!-- Chat messages will be added here -->
        </div>
        <div id="update-box">
            Last Update: Integrated with Gemini 1.5
        </div>
    </div>
    <div class="side-panel">
        <div id="clock"></div>
        <div class="memory">
            <h3 onclick="toggleCollapsible('memory-list')">Memory ▲</h3>
            <ul id="memory-list">
                <li>Name: </li>
                <li>Relationship: Human friend</li>
            </ul>
        </div>
    </div>
</div>

<script>
let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = true;
recognition.interimResults = true;

let listening = false;
let lastSpeechTime = Date.now();
const SPEECH_DELAY = 2000; // 2 seconds delay

const synth = window.speechSynthesis;

function speak(text) {
    if (synth) {
        const utterance = new SpeechSynthesisUtterance(text);
        synth.speak(utterance);
    }
}

async function sendMessage(message) {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML += `<p class="user-message">User: ${message}</p>`;
    chatWindow.scrollTop = chatWindow.scrollHeight;

    document.getElementById('status').textContent = "Status: Thinking...";

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const aiResponse = `Amara: ${data.response}`;
        chatWindow.innerHTML += `<p class="ai-message">${aiResponse}</p>`;
        chatWindow.scrollTop = chatWindow.scrollHeight;
        speak(aiResponse);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = `Amara: I'm sorry, I encountered an error while processing your request. Could you please try again?`;
        chatWindow.innerHTML += `<p class="ai-message">${errorMessage}</p>`;
        speak(errorMessage);
    }

    document.getElementById('status').textContent = "Status: Ready";
}

function addReminder(text) {
    const reminderList = document.getElementById('reminder-list');
    const li = document.createElement('li');
    li.className = 'reminder-item';
    li.innerHTML = `
        <span>${text}</span>
        <button onclick="removeReminder(this)">Remove</button>
    `;
    reminderList.appendChild(li);
}

function removeReminder(button) {
    button.parentElement.remove();
}

function toggleCollapsible(id) {
    const element = document.getElementById(id);
    element.classList.toggle('collapsible-inactive');
    const header = element.previousElementSibling;
    if (element.classList.contains('collapsible-inactive')) {
        header.innerHTML = header.innerHTML.replace('▲', '▼');
    } else {
        header.innerHTML = header.innerHTML.replace('▼', '▲');
    }
}

recognition.onresult = (event) => {
    const result = event.results[event.results.length - 1];
    const transcript = result[0].transcript.trim().toLowerCase();

    if (transcript === "pause") {
        listening = false;
        document.getElementById('status').textContent = "Status: Offline";
        document.getElementById('info').textContent = "Jacked out for now. Say 'Hey Amara' to plug back in.";
        document.getElementById('voice-indicator').classList.remove('listening');
    } else if (transcript === "hey amara") {
        listening = true;
        document.getElementById('status').textContent = "Status: Jacked In";
        document.getElementById('info').textContent = "I'm back online! What's the buzz?";
        document.getElementById('voice-indicator').classList.add('listening');
    } else if (listening && result.isFinal) {
        const now = Date.now();
        if (now - lastSpeechTime > SPEECH_DELAY) {
            sendMessage(transcript);
        }
        lastSpeechTime = now;
    }
};

recognition.onend = () => {
    recognition.start();
};

window.onload = function() {
    function updateClock() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        const timeString = `${hours}:${minutes}:${seconds} ${ampm}`;
        document.getElementById('clock').textContent = timeString;
    }

    updateClock();
    setInterval(updateClock, 1000);

    // Start speech recognition
    recognition.start();

    // Speak initial message on page load
    speak("Hey User! I'm Amara, your AI assistant. What's on your name?");
};

</script>

</body>
</html>
'''

# Run the Flask app with ngrok
if __name__ == '__main__':
    # Start ngrok to tunnel the local Flask app to a public URL
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:5000\"".format(public_url))

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
