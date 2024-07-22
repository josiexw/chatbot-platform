import React, { useState } from 'react';
import Chat from './chatbot/Chat';
import ChatBubbleIcon from './chatbot/ChatBubbleIcon';

const PreviewAssistant = ({ selectedAssistant, onClose }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleChatToggle = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="popup">
      <div className="popup-inner">
        <button className="close-button" onClick={onClose}>Close</button>
        <h2>Preview Assistant: {selectedAssistant.name}</h2>
        {isChatOpen && <Chat assistantId={selectedAssistant.id} handleClose={handleChatToggle} />}
        <ChatBubbleIcon assistantId={selectedAssistant.id} handleClick={handleChatToggle} />
      </div>
    </div>
  );
};

export default PreviewAssistant;
