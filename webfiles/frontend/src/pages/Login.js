import React, { useState } from 'react';
import "./styles/login.css";
import { loginUser } from "../api";
import { useNavigate } from 'react-router-dom';


function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log('Form submitted');
    console.log('Logging in with:', username, password);
    
    try {
      const response = await loginUser(username, password);
      console.log("Login response: ", response);
      sessionStorage.setItem("username", response.username);
      // This is where you would navigate to a different page because successful
      console.log("login successful from front end");
      navigate('/'); // route to Home.js
      
    } catch (err) {
      console.log("Invalid credentials");
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div className="banner">
        <h1>Welcome Back! Please Log-In Below:</h1>
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
      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
