import React, { useState } from 'react';
import "./styles/login.css";
import { createUser } from "../api";
import { useNavigate } from 'react-router-dom';

function CreateUser() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState(null); // null = not selected
  const navigate = useNavigate();
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    const role_id = role === 3 ? 3 : 2; // Vendor is 3, Customer is 2, default to 2
    console.log('Creating account with:', username, password, email, role_id);

    try {
      const response = await createUser(username, password, email, role_id);
      localStorage.setItem("username", response.username);
      console.log("Creation successful from front end");
      navigate('/login');
      window.location.reload();
    } catch (err) {
      console.log("Error from creation", err);
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
      <div>
      <button
          type="button"
          onClick={() => setRole(2)}
          className={role === 2 ? 'selected' : ''}
        >
          Customer
        </button>

        <button
          type="button"
          onClick={() => setRole(3)}
          className={role === 3 ? 'selected' : ''}
        >
          Vendor
        </button>
      </div>
      <button type="submit">Create Account</button>
    </form>
  );
}

export default CreateUser;
