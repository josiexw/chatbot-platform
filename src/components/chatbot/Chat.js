import React, { useState, useEffect, useRef } from 'react';
import { TextField, Container, Grid, AppBar, Toolbar, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import CloseIcon from '@mui/icons-material/Close';
import Message from './Message';
import { MessageDto } from "./MessageDto";
import axios from 'axios';
import ChatIcon from '@mui/icons-material/Chat';

const Chat = ({ assistantId, handleClose }) => {
  const [isWaiting, setIsWaiting] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [assistant, setAssistant] = useState(null);
  const [chatTitle, setChatTitle] = useState("");
  const [headerColor, setHeaderColor] = useState(null);
  const [assistantColor, setAssistantColor] = useState(null);
  const [userColor, setUserColor] = useState(null);
  const [threadId, setThreadId] = useState(null);
  const [shouldSendMessage, setShouldSendMessage] = useState(false);
  const messagesEndRef = useRef(null);
  const hasInitializedRef = useRef(false);

  useEffect(() => {
    if (!hasInitializedRef.current) {
      initChatBot();
      hasInitializedRef.current = true;
    }
  }, []);

  // Initialize chatbot on backend
  const fetchAssistant = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/get_preview', { input: assistantId });
      const data = response.data;
      setChatTitle(data.title);
      setHeaderColor(data.header_color);
      setAssistantColor(data.assistant_color);
      setUserColor(data.user_color);
      messages.push(createNewMessage(data.assistant_start_message, false, data.assistant_color));
      for (var i = 0; i < data.suggested_responses.length; i++) {
        messages.push(createNewMessage(data.suggested_responses[i], false, null, true))
      }
      setMessages([...messages]);
      await axios.post('http://127.0.0.1:8000/api/get_assistant', { input: assistantId });
      setAssistant(data.assistant_id);
    } catch (error) {
      console.error('Error fetching assistant:', error);
    }
  };

  // Send a message and receive the chatbot's response
  const fetchMessage = async (input) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/send_message', {
        input,
        'assistant_id': assistant,
        'thread_id': threadId
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching message response:', error)
    }
  };

  const initChatBot = async () => {
    await fetchAssistant();
    console.log("Assistant initialized")
  };

  const createNewMessage = (content, isUser, color, isSuggested=false) => {
    return new MessageDto(isUser, content, color, isSuggested);
  };

  const handleSendMessage = async () => {
    if (!assistant) {
      console.warn('Assistant is not initialized yet.');
      return;
    }
    messages.push(createNewMessage(input, true, userColor));
    setMessages([...messages]);
    setInput("");

    setIsWaiting(true);
    const data = await fetchMessage(input);
    setThreadId(data.thread_id)
    setIsWaiting(false);

    if (data.response) {
      setMessages([...messages, createNewMessage(data.response, false, assistantColor)]);
    } else {
      console.error('No response from the assistant.');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    if (shouldSendMessage) {
      handleSendMessage();
      setShouldSendMessage(false);
    }
  }, [input]);

  const handleSuggestedMessageClick = (content) => {
    setInput(content);
    setShouldSendMessage(true);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Container style={{ 
      position: 'fixed', 
      bottom: '80px',
      right: '20px', 
      width: '350px',
      height: '500px',
      display: 'flex',
      flexDirection: 'column', 
      border: '1px solid #ddd',
      boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)', 
      backgroundColor: 'white',
      padding: 0,
      margin: 0
    }}>
      <AppBar position="static" sx={{ backgroundColor: headerColor, width: '100%' }}>
        <Toolbar>
          <h3 style={{ flexGrow: 1, marginTop: '12px' }}>{chatTitle}</h3>
          <IconButton edge="end" color="inherit" onClick={handleClose}>
            <CloseIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Grid direction="column" style={{ flexGrow: 1, overflowY: 'auto', padding: '16px' }}>
        {messages.map((message, index) => (
          <Message key={index} message={message} onMessageClick={handleSuggestedMessageClick} />
        ))}
        <div ref={messagesEndRef} />
      </Grid>
      <Grid direction="column" style={{flexGrow: 1}}>
        {isWaiting && (
            <div style={{ position: 'absolute', bottom: '100px', left: '20px' }}>
              <CircularProgress size={18} />
            </div>
          )}
      </Grid>
      <Grid container item spacing={2} style={{ padding: '16px' }}>
        <Grid item xs={10}>
          <TextField
            label="Type your message"
            variant="outlined"
            fullWidth
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
        </Grid>
        <Grid item xs={2}>
          <IconButton onClick={handleSendMessage} style={{ color: headerColor, marginTop: '8px' }}>
            <SendIcon />
          </IconButton>
        </Grid>
      </Grid>
      <IconButton
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
        }}>
        <ChatIcon />
      </IconButton>
    </Container>
  );
};

export default Chat;
