import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CreateAssistant = ({ onClose }) => {
  const [formHTML, setFormHTML] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchForm();
  }, []);

  const fetchForm = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/make_assistant');
      setFormHTML(response.data.form_html);
    } catch (error) {
      console.error('Error fetching form:', error);
      alert('Error fetching form. Please try again.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formElement = document.getElementById('assistant-form');
    const formData = new FormData(formElement);

    setIsSaving(true);

    try {
      await axios.post('http://127.0.0.1:8000/api/make_assistant', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert('Assistant created successfully!');
      onClose();
    } catch (error) {
      console.error('Error creating assistant:', error);
      alert('Error creating assistant. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="popup">
      <div className="popup-inner">
        <form id="assistant-form" onSubmit={handleSubmit}>
          <div dangerouslySetInnerHTML={{ __html: formHTML }} />
          {!isSaving ? (
            <button type="submit">Save</button>
          ) : (
            <p>Saving...</p>
          )}
        </form>
        <button className="close-button" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default CreateAssistant;
