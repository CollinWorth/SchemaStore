import "./styles.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login"

function App() {
  return (
    <Router>
      <div className="app">
      <nav className="sidebar">
        <h2>Schema Store</h2>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/login">Login</Link></li>
        </ul>
      </nav>

      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
