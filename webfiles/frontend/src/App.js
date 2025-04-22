import "./styles.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Cart from "./pages/Cart";
import AccountDashboard from "./pages/AccountDashboard";
import About from "./pages/About";
import Create_Account from "./pages/Create_Account";
import Products from "./pages/Products";
import { Car, Search } from "lucide-react";
import logo from "./images/logo.png";
import Admin from "./pages/Admin";
import Payment from "./pages/Payment";

function App() {
  const username = sessionStorage.getItem("username");
  const role_id = sessionStorage.getItem("role_id");

  return (
    <Router>
     
      <div className="app">
        {/* Top Navbar */}
        <nav className="navbar">
          {/* Clickable Logo (Redirects to Home) */}
          <div className="navbar-left">
          <Link to="/" className="logo">
            <img src={logo} alt="Schema Store Logo" className="logo-image" />
          </Link> 
            <Link className="nav-link" to="/about">About Us</Link>
            <Link className="nav-link" to="/products">Search</Link>
          </div>

          {/* Search Bar */}
          {/*<div className="search-container">
            <Search className="search-icon" size={20} />
            <input type="text" placeholder="Search..." className="search-input" />
          </div>
          <Link to="/products"><span>Search</span></Link>

          {/* Navigation Links */}
          <ul className="nav-links">
            {!username && (
              <>
                <li><Link to="/login">Login</Link></li>
                <li><Link to="/create_account">Create Account</Link></li>
              </>
            )}

            {username && (
              <>
                <li><Link to="/accountdashboard">Account</Link></li>
              </>
            )}

            {/* Cart is always visible */}
            <li><Link to="/cart">Cart</Link></li>

            {/* Admin link only if logged in and role_id == 1 */}
            {username && role_id === "1" && (
              <li><Link to="/admin">Admin</Link></li>
            )}
          </ul>
        </nav>

        {/* Main Content */}
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/create_account" element={<Create_Account />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/accountdashboard" element={<AccountDashboard />} />
            <Route path="/products" element={<Products />} />
            <Route path="/about" element={<About />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/payment" element={<Payment />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
} export default App;