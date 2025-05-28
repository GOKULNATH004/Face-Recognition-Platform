import React, { useState } from 'react';
import RegistrationTab from './components/RegistrationTab';
import LiveRecognitionTab from './components/LiveRecognitionTab';
import ChatTab from './components/ChatTab';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('registration');

  const renderTab = () => {
    switch (activeTab) {
      case 'registration': return <RegistrationTab />;
      case 'recognition': return <LiveRecognitionTab />;
      case 'chat': return <ChatTab />;
      default: return null;
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Face AI Portal</h1>
        <nav className="nav-bar">
          <button className={activeTab === 'registration' ? 'active' : ''} onClick={() => setActiveTab('registration')}>Register</button>
          <button className={activeTab === 'recognition' ? 'active' : ''} onClick={() => setActiveTab('recognition')}>Recognition</button>
          <button className={activeTab === 'chat' ? 'active' : ''} onClick={() => setActiveTab('chat')}>ChatBot</button>
        </nav>
      </header>
      <main className="main-section">
        {renderTab()}
      </main>
    </div>
  );
}
