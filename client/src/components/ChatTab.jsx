import React, { useState, useEffect } from 'react';

export default function ChatTab() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: "You", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const res = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input })
    });
    const data = await res.json();
    const botMsg = { sender: "AI", text: data.answer };
    setMessages((prev) => [...prev, botMsg]);
    setInput("");
  };

  return (
    <div className="tab-content">
      <h2>Ask About Face Logs</h2>
      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`chat-message ${m.sender === 'You' ? 'user' : 'ai'}`}>
            <strong>{m.sender}:</strong> {m.text}
          </div>
        ))}
      </div>
      <div className="chat-input-container">
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask e.g. who was registered last..."
        />
        <button className="send-btn" onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
