import React, { useState } from 'react';
import axios from 'axios';

const DatabaseTest = () => {
  const [message, setMessage] = useState('');

  const testDatabaseConnection = async () => {
    try {
      const response = await axios.get('http://localhost:8000/test_connection');
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error connecting to the database');
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <button onClick={testDatabaseConnection}>Test Database Connection</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default DatabaseTest;