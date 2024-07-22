// src/components/Message.js
import React from 'react';
import PropTypes from 'prop-types';

const Message = ({ message }) => {
  return (
    <div style={{ textAlign: message.isUser ? 'right' : 'left', margin: '8px' }}>
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
        {message.content.split('\n').map((text, index) => (
          <React.Fragment key={index}>
            {text}
            <br />
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

Message.propTypes = {
  message: PropTypes.shape({
    isUser: PropTypes.bool.isRequired,
    content: PropTypes.string.isRequired,
  }).isRequired,
};

export default Message;
