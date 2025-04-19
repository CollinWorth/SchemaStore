import React, { useState } from 'react';
import "./styles/login.css";
import { createUser } from "../api";
import { useNavigate } from 'react-router-dom';


function CreateUser() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log('Form submitted');
    // Handle login logic here (e.g., API call)
    console.log('Creating account with:', username, password, email);
    try {
      const response = await createUser(username, password, email);
      localStorage.setItem("username", response.username);
      // This is where you would navigate to a different page because successful
      console.log("Creation successful from front end");
      navigate('/Home.js'); // route to Home.js
    } catch (err) {
      console.log("Error from creation");
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div className="banner">
        <h1>Welcome! Please Create a Username and Password Below:</h1>
      </div>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="text"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
}

export default CreateUser;