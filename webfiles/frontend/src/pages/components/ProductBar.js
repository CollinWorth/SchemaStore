import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ProductBar.css";

export default function ProductBar() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/products")
      .then((response) => setProducts(response.data))
      .catch((error) => console.error("Error fetching products:", error));
  }, []);

  return (
    <div className="product-bar">
      {products.map((product) => (
        <div key={product.id} className="product-card">
          <img src={product.image_url} alt={product.name} className="product-image" />
          <div className="product-info">
            <h4>{product.name}</h4>
            <p>${product.price.toFixed(2)}</p>
          </div>
        </div>
      ))}
    </div>
  );
}