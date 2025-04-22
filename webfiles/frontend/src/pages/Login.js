import React, { useState } from 'react';
import "./styles/login.css";
import { loginUser } from "../api";
import { useNavigate } from 'react-router-dom';
import axios from "axios";


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
  
      // 🔥 NEW: Fetch user info to get the role
      const userInfo = await axios.get(`http://127.0.0.1:8000/user/${response.username}`);
      console.log("User Info:", userInfo.data);
  
      // Map role string to role_id
      const roleMap = {
        "admin": 1,
        "buyer": 2,
        "seller": 3
      };
      const role_id = roleMap[userInfo.data.role];
  
      sessionStorage.setItem("role_id", role_id);
  
      console.log("login successful from front end");
      navigate('/');
      window.location.reload();
      
    } catch (err) {
      console.log("Invalid credentials");
    }
  };
  
  return (
    <div>
      <div className="banner">
        <h1>Welcome Back! Please Log-In Below:</h1>
      </div>
    <div className='login-container'>
    <form onSubmit={handleSubmit}>
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
    </div>
    </div>
  );
}

export default Login;
