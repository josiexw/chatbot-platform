import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CreateAssistant from './CreateAssistant';
import PreviewAssistant from './PreviewAssistant';
import EmbedAssistant from './EmbedAssistant';

const Dashboard = () => {
  const [assistants, setAssistants] = useState([]);
  const [showPreview, setShowPreview] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [showEmbed, setShowEmbed] = useState(false);
  const [selectedAssistant, setSelectedAssistant] = useState(null);

  useEffect(() => {
    fetchAssistants();
  }, []);

  const fetchAssistants = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/list_assistants');
      setAssistants(response.data);
    } catch (error) {
      console.error('Error fetching assistants:', error);
    }
  };

  const handlePreview = (assistant) => {
    setSelectedAssistant(assistant);
    setShowPreview(true);
  };

  const handleDelete = async (assistant) => {
    if (window.confirm(`Are you sure you want to delete assistant: ${assistant.name}?`)) {
      try {
        const formData = new FormData();
        formData.append('assistant_id', assistant.id);

        await axios.post('http://127.0.0.1:8000/api/delete_assistant', formData);
        fetchAssistants();
      } catch (error) {
        console.error('Error deleting assistant:', error);
        alert('Failed to delete assistant. Please try again.');
      }
    }
  };

  const handleEmbed = (assistant) => {
    setSelectedAssistant(assistant);
    setShowEmbed(true);
  };

  const handleCreate = () => {
    setShowCreate(true);
  };

  const closeCreatePopup = () => {
    setShowCreate(false);
    fetchAssistants();
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <button onClick={handleCreate}>Create Assistant</button>

      {assistants.map((assistant) => (
        <div key={assistant.id}>
          <h3>{assistant.name}</h3>
          <p>Assistant ID: {assistant.id}</p>
          <p>{assistant.instructions}</p>
          <button onClick={() => handlePreview(assistant)}>Preview</button>
          <button onClick={() => handleEmbed(assistant)}>Embed</button>
          <button onClick={() => handleDelete(assistant)}>Delete</button>
        </div>
      ))}

      {showPreview && (
        <PreviewAssistant
          selectedAssistant={selectedAssistant}
          onClose={() => setShowPreview(false)}
        />
      )}

      {showEmbed && (
        <EmbedAssistant
          assistant={selectedAssistant}
          onClose={() => setShowEmbed(false)}
        />
      )}

      {showCreate && (
        <CreateAssistant onClose={closeCreatePopup} />
      )}
    </div>
  );
};

export default Dashboard;
