import React, { useState, useEffect } from 'react';
import { IconButton } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import axios from 'axios';

const ChatBubbleIcon = ({ assistantId, handleClick }) => {
  const [headerColor, setHeaderColor] = useState(null);

  useEffect(() => {
    fetchHeaderColor();
  }, []);

  const fetchHeaderColor = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/get_assistant', { input: assistantId });
      const data = response.data;
      setHeaderColor(data.header_color);
    } catch (error) {
      console.error('Error fetching header color:', error);
    }
  };

  return (
    <IconButton
      onClick={handleClick}
      style={{
        position: 'fixed',
        bottom: '16px',
        right: '16px',
        backgroundColor: headerColor,
        color: 'white',
        borderRadius: '50%',
        width: '56px',
        height: '56px',
        boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)'
      }}
    >
      <ChatIcon />
    </IconButton>
  );
};

export default ChatBubbleIcon;
