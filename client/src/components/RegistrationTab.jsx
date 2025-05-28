import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import './styles.css';

export default function RegistrationTab() {
  const webcamRef = useRef(null);
  const [name, setName] = useState("");
  const [id, setId] = useState("");

  const captureAndSend = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const payload = { name, id, image: imageSrc };
    await fetch("http://localhost:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    alert("Face registered!");
    setName("");
    setId("");
  };

  return (
    <div className="tab-content">
      <h2>📸 Register Face</h2>
      <Webcam ref={webcamRef} screenshotFormat="image/jpeg" width={320} height={240} />
      <div className="form-group">
        <input className="input-box" type="text" placeholder="Enter Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input className="input-box" type="text" placeholder="Enter ID" value={id} onChange={(e) => setId(e.target.value)} />
        <button className="send-btn" onClick={captureAndSend}>Capture & Register</button>
      </div>
    </div>
  );
}