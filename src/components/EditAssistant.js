import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EditAssistant = ({ assistant, onClose }) => {
  const [formHTML, setFormHTML] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchForm();
  }, []);

  const fetchForm = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/edit_assistant', {params: { assistant_id: assistant.id }});
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
    formData.append('assistant_id', assistant.id);

    setIsSaving(true);

    try {
      await axios.post('http://127.0.0.1:8000/api/edit_assistant', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      onClose();
    } catch (error) {
      console.error('Error editing assistant:', error);
      alert('Error editing assistant. Please try again.');
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

export default EditAssistant;
