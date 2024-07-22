import React from 'react';

const EmbedAssistant = ({ assistant, onClose }) => {
  const embedCode =
  `<div id="chatbot-container"></div>
    <script src="https://josiexw.github.io/chatbot-widget/static/js/main.f03bb32e.js?assistantId=${assistant.id}"></script>
    <script>
        ChatbotWidget.init({ someConfig: 'value' }, document.getElementById('chatbot-container'));
    </script>`;

  return (
    <div className="popup">
      <div className="popup-inner">
        <button className="close-button" onClick={onClose}>Close</button>
        <h2>Embed Assistant: {assistant.name}</h2>
        <pre>
          <code>{embedCode}</code>
        </pre>
      </div>
    </div>
  );
};

export default EmbedAssistant;
