import React, { useEffect, useState } from 'react';
import "./styles/login.css";
import axios from "axios";

function Login() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [users, setUsers] = useState([]);
  
    const handleSubmit = (event) => {
      event.preventDefault();
      // Handle login logic here (e.g., API call)
      console.log('Logging in with:', username, password);
    };

    useEffect(() => {
      axios.get("http://127.0.0.1:8000/users")
        .then((response) => setUsers(response.users))
        .catch((error) => console.error("Error fetching login page:", error));
    }, []);

    
  
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