import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import './styles.css';

export default function LiveRecognitionTab() {
  const webcamRef = useRef(null);
  const [results, setResults] = useState([]);

  const recognizeFace = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const res = await fetch("http://localhost:5000/recognize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageSrc }),
    });
    const data = await res.json();
    setResults(data.results);
  };

  return (
    <div className="tab-content">
      <h2>🎥 Face Recognition</h2>
      <Webcam ref={webcamRef} screenshotFormat="image/jpeg" width={320} height={240} />
      <button className="send-btn" onClick={recognizeFace}>Recognize Face</button>
      <div className="results-container">
        {results.map((r, i) => (
          <div className="result-card" key={i}>
            <p><strong>Name:</strong> {r.name}</p>
            <p><strong>ID:</strong> {r.id}</p>
            <p><strong>Time:</strong> {r.timestamp}</p>
          </div>
        ))}
      </div>
    </div>
  );
}