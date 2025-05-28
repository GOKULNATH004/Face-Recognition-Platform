# Face Recognition and AI Chatbot Platform

This project is a browser-based face recognition and AI chatbot system built for the Katomaran AI Hackathon. It allows real-time face registration and recognition, stores metadata securely, and integrates with the OpenAI API for intelligent chatbot responses based on the user database.

---

## Features

- 📸 **Face Registration** using webcam with name, ID, and timestamp logging  
- 🎯 **Face Recognition** in real-time using DeepFace and webcam feed  
- 🧠 **AI Chatbot** powered by OpenAI API for user queries about face registrations  
- 🗃️ **Metadata Storage** in SQLite database  
- 🌐 **Full-Stack Architecture** using React.js (frontend) and FastAPI (backend)  

---

## Tech Stack

- **Frontend:** React.js  
- **Backend:** FastAPI  
- **Database:** SQLite3  
- **AI Models:** DeepFace (for recognition), OpenAI (for chat)  
- **Camera Access:** via react-webcam  
- **Face Analysis:** DeepFace with RetinaFace backend  

---

## Folder Structure

📁 d2/
├── ai/               
│   ├── api_server.py
│   └── db/
├── client/           
│   └── src/components
│       ├── RegistrationTab.jsx
│       ├── LiveRecognitionTab.jsx
│       ├── ChatTab.jsx
├── registered_faces/ 

---

##Acknowledgement
This project is a part of a hackathon run by Katomaran [https://katomaran.com]
