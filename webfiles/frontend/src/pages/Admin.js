import React, { useEffect, useState } from "react";
import axios from "axios";
import "./styles/login.css";
import ProductBar from "./components/ProductBar"; 

function Admin() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [users, setUsers] = useState([]);

  const [newProduct, setNewProduct] = useState({
    sku: "",
    name: "",
    description: "",
    price: 0,
    stock: 0,
    img: null // <- always null for now
  });

  useEffect(() => {
    fetchProducts();
    fetchUsers();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/products/");
      setProducts(response.data);
    } catch (err) {
      console.error("Failed to fetch products", err);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/user/");
      const usersWithRoles = response.data.map(user => ({
        ...user,
        role: mapRole(user.role)
      }));
      setUsers(usersWithRoles);
    } catch (err) {
      console.error("Failed to fetch users", err);
      setUsers([]);
    }
  };

  const mapRole = (roleId) => {
    switch (roleId) {
      case 1:
        return "Admin";
      case 2:
        return "Buyer";
      case 3:
        return "Seller";
      default:
        return "Unknown";
    }
  };

  const handleDeleteUser = async (username) => {
    if (!window.confirm(`Are you sure you want to delete user "${username}"?`)) {
      return; // Cancel if user says no
    }
    
    try {
      await axios.delete(`http://127.0.0.1:8000/user/`, {
        params: { username: username }
      });
      fetchUsers(); // Refresh the list after delete
    } catch (err) {
      console.error("Failed to delete user", err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct((prev) => ({
      ...prev,
      [name]: name === "price" || name === "stock" ? Number(value) : value
    }));
  };

  const handleCreateProduct = async () => {
    const formData = new FormData();
    formData.append('sku', newProduct.sku);
    formData.append('name', newProduct.name);
    formData.append('description', newProduct.description);
    formData.append('price', newProduct.price.toString());
    formData.append('stock', newProduct.stock.toString());
  
    if (newProduct.img) {
      formData.append('file', newProduct.img);
    } else {
      // Send a fake empty file if no image
      const emptyFile = new Blob([], { type: 'image/png' });
      formData.append('file', emptyFile, 'empty.png');
    }
  
    try {
      await axios.post("http://127.0.0.1:8000/products/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      fetchProducts();
      setShowModal(false);
      setNewProduct({ sku: "", name: "", description: "", price: 0, stock: 0, img: null });
    } catch (err) {
      console.error("Error creating product", err);
    }
  };

  return (
    <div className="admin">
      <h1>Admin Page</h1>

      <h2>Products:</h2>

      {loading ? <p>Loading...</p> : (
        <table className="product-table">
          <thead>
            <tr>
              <th>SKU</th>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Image URL</th>
            </tr>
          </thead>
          <tbody>
            {products.map((prod, index) => (
              <tr key={index}>
                <td>{prod.sku}</td>
                <td>{prod.name}</td>
                <td>{prod.description}</td>
                <td>${prod.price}</td>
                <td>{prod.stock}</td>
                <td>{prod.img ? "Image exists" : "No image"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <button onClick={() => setShowModal(true)}>Create New Product</button>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Create Product</h3>
            <input name="sku" placeholder="SKU" onChange={handleInputChange} />
            <input name="name" placeholder="Name" onChange={handleInputChange} />
            <input name="description" placeholder="Description" onChange={handleInputChange} />
            <input name="price" placeholder="Price" type="number" onChange={handleInputChange} />
            <input name="stock" placeholder="Stock" type="number" onChange={handleInputChange} />
            {/* File input removed */}
            <button onClick={handleCreateProduct}>Submit</button>
            <button onClick={() => setShowModal(false)}>Cancel</button>
          </div>
        </div>
      )}

      <h2>Users:</h2>

      {loading ? <p>Loading...</p> : (
        <table className="user-table">
            <thead>
            <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th> {/* 👈 NEW */}
            </tr>
            </thead>
            <tbody>
                {users.map((user, index) => (
                    <tr key={index}>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td>
                        <button onClick={() => handleDeleteUser(user.username)}>Delete</button>
                    </td>
                    </tr>
                ))}
                </tbody>
        </table>
        )}
        </div>
    );
    }

export default Admin;
