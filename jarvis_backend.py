import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import webbrowser 
import pywhatkit
import threading
import time
from PIL import Image, ImageTk  # For handling images (like microphone animation)

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak text
def speak(text, display_label):
    engine.say(text)
    engine.runAndWait()
    display_label.config(text=f"Jarvis: {text}")

# Function to handle web navigation and searches
def process_web_command(command, display_label):
    command = command.lower()

    if "open" in command:
        if "google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google", display_label)
        elif "youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube", display_label)
        elif "facebook" in command:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook", display_label)
        elif "linkedin" in command:
            webbrowser.open("https://www.linkedin.com")
            speak("Opening LinkedIn", display_label)
        else:
            site = command.replace("open ", "").strip()
            webbrowser.open(f"https://{site}.com")
            speak(f"Opening {site}", display_label)

    elif "search" in command or "who is" in command or "what is" in command:
        query = command.replace("search", "").replace("who is", "").replace("what is", "").strip() 
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}", display_label)

    elif "on wikipedia" in command:
        query = command.replace("search", "").replace("on wikipedia", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
        speak(f"Searching Wikipedia for {query}")

    elif "on youtube" in command:
        query = command.replace("search", "").replace("on youtube", "").strip()
        pywhatkit.playonyt(query)  # Play the song directly from YouTube
        speak(f"Playing {query} on YouTube", display_label)

    elif "on spotify" in command:
        query = command.replace("search", "").replace("on spotify", "").strip()
        webbrowser.open(f"https://open.spotify.com/search/{query}")
        speak(f"Searching Spotify for {query}", display_label)

    elif "on soundcloud" in command:
        query = command.replace("search", "").replace("on soundcloud", "").strip()
        webbrowser.open(f"https://soundcloud.com/search?q={query}")
        speak(f"Searching SoundCloud for {query}", display_label)

    else:
        speak("Sorry, I couldn't understand that request.", display_label)

# Function to listen for wake word
def listen_for_wake_word():
    try:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            return "jarvis" in command
    except Exception as e:
        print(f"Wake word detection error: {e}")
        return False

# Function to listen for user commands
def listen_for_command(display_label):
    try:
        with sr.Microphone() as source:
            print("Jarvis is active. Listening for your command...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            display_label.config(text=f"You: {command}")
            return command
    except Exception as e:
        print(f"Command error: {e}")
        speak("Sorry, I didn't catch that.", display_label)
        return None

# Function to process commands
def process_command(command, display_label):
    if "play" in command:
        song_name = command.replace("play", "").strip()
        speak(f"Playing {song_name}...", display_label)
        process_web_command(f"search {song_name} on youtube", display_label)  # Searching and playing the song on YouTube by default
    elif "exit" in command or "quit" in command:
        speak("Goodbye!", display_label)
        window.quit()
    else:
        process_web_command(command, display_label)

# Function for listening and responding in the background
def listen_and_respond(display_label, mic_label):
    while True:
        if listen_for_wake_word():
            mic_label.config(image=microphone_active)  # Animation start
            speak("Yes?", display_label)
            user_command = listen_for_command(display_label)
            if user_command:
                process_command(user_command, display_label)
            mic_label.config(image=microphone_idle)  # Animation stop

# Create the main window
window = tk.Tk()
window.title("Jarvis AI Assistant")
window.geometry("500x300")
window.config(bg="white")

# Create a label for displaying Jarvis responses
response_label = tk.Label(window, text="Jarvis: Hello! How can I assist you?", font=("Arial", 14), bg="white")
response_label.pack(pady=10)

# Create a label for displaying user input
user_input_label = tk.Label(window, text="You: Waiting for wake word...", font=("Arial", 12), bg="white")
user_input_label.pack(pady=5)

# Load microphone images for animation
microphone_idle = ImageTk.PhotoImage(Image.open("microphone_idle.png").resize((50, 50)))
microphone_active = ImageTk.PhotoImage(Image.open("microphone_active.png").resize((50, 50)))

# Create a label for microphone animation
mic_label = tk.Label(window, image=microphone_idle, bg="white")
mic_label.pack(pady=20)

# Start listening in the background
listen_thread = threading.Thread(target=listen_and_respond, args=(response_label, mic_label))
listen_thread.daemon = True
listen_thread.start()

# Run the main loop 
window.mainloop()




