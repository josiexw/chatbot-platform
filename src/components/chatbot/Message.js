import './Message.css';
import React from 'react';
import PropTypes from 'prop-types';

const Message = ({ message, onMessageClick }) => {
  const handleClick = () => {
    if (message.isSuggested) {
      onMessageClick(message.content);
    }
  };

  const messageClass = message.isSuggested ? 'suggested-message' : (message.isUser ? 'user-message' : 'other-message');

  return (
    <div className="message-container" onClick={handleClick} style={{ textAlign: message.isUser ? 'right' : 'left' }}>
      <div style={{ 
        display: 'inline-block', 
        backgroundColor: message.color, 
        padding: '10px', 
        borderRadius: '14px', 
        color: 'white',
        maxWidth: '80%',
        wordWrap: 'break-word',
        textAlign: 'left'
      }}>
        <div className={messageClass}>
          {message.content.split('\n').map((text, index) => (
            <React.Fragment key={index}>
              {text}
              <br />
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
};

Message.propTypes = {
  message: PropTypes.shape({
    isUser: PropTypes.bool.isRequired,
    content: PropTypes.string.isRequired,
    isSuggested: PropTypes.bool
  }).isRequired,
  onMessageClick: PropTypes.func.isRequired,
};

export default Message;
