import React, { useEffect, useState } from "react";
import axios from "axios";
import "./styles/login.css";
import ProductBar from "./components/ProductBar";

function Seller(){
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    const [newProduct, setNewProduct] = useState({
        sku: "",
        name: "",
        description: "",
        price: 0,
        stock: 0,
        img: "" // <-- initialize as empty string
      });

    useEffect(() => {
        fetchProducts();
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

    const handleDeleteProduct = async (sku) => {
        if (!window.confirm(`Are you sure you want to delete product with SKU "${sku}"?`)) {
          return;
        }
    
        try {
          await axios.delete(`http://127.0.0.1:8000/products/${sku}`);
          fetchProducts(); // Refresh product list
        } catch (err) {
          console.error("Failed to delete product", err);
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
        formData.append('img_url', newProduct.img);  // sending image URL string
      
        try {
            await axios.post("http://127.0.0.1:8000/products/", formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            });
            fetchProducts();
            setShowModal(false);
            setNewProduct({ sku: "", name: "", description: "", price: 0, stock: 0, img: "" });
          } catch (err) {
            console.error("Error creating product", err);
          }
        };

        return (
            <div>
                <h1>Seller Page</h1>
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
              <th>Delete</th> 
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
                <td>
                  {prod.img ? (
                  <img 
                    src={prod.img} 
                    alt={prod.name} 
                    style={{ maxWidth: "100px", maxHeight: "100px", objectFit: "contain" }} 
                  />
                  ) : (
                    "No image"
                  )}
                </td>
                <td>
                  <button onClick={() => handleDeleteProduct(prod.sku)} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                    🗑️
                  </button>
                </td>
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
                <input name="sku" placeholder="SKU" onChange={handleInputChange} value={newProduct.sku} />
                <input name="name" placeholder="Name" onChange={handleInputChange} value={newProduct.name} />
                <input name="description" placeholder="Description" onChange={handleInputChange} value={newProduct.description} />
                <input name="price" placeholder="Price" type="number" onChange={handleInputChange} value={newProduct.price} />
                <input name="stock" placeholder="Stock" type="number" onChange={handleInputChange} value={newProduct.stock} />
                <input
                  name="img"
                  placeholder="Image URL"
                  onChange={handleInputChange}
                  value={newProduct.img}
                />
                <button onClick={handleCreateProduct}>Submit</button>
                <button onClick={() => setShowModal(false)}>Cancel</button>
              </div>
            </div>
          )}
            </div>
        );

    
    
    
} export default Seller;