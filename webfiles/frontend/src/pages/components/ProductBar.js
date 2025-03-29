import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ProductBar.css";
import { useCart } from './Cartcomp';
import { getProducts } from "D:/Git projects/GitProjects/SchemaStore/webfiles/frontend/src/api.js";

import sneakers from "../assets/sneakers.jpg";
import joggers from "../assets/joggers.jpg";
import sweatshirt from "../assets/sweatshirt.jpg"
import sunglasses from "../assets/sunglasses.jpg"

const products = [ //Place holder for items, so that we have some images
  {id: 1, name: "Sneakers", price: 79.99, image: sneakers, category: "shoes"},
  {id: 2, name: "Joggers", price: 49.99, image: joggers, category: "bottoms"},
  {id: 3, name: "Sweatshirt", price: 59.99, image: sweatshirt, category: "tops"},
  {id: 4, name: "Sunglasses", price: 39.99, image: sunglasses, category: "accessories"},
]

const ProductBar = ({ overrideProducts, category}) => {
  const { addToCart } = useCart();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const allProducts = await getProducts();
        setProducts(allProducts);
      } catch (error) {
        console.error("Failed to load products", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

const filteredProducts = overrideProducts 
?overrideProducts
:category
? products.filter(p => p.category === category)
: products;
if (loading) return <p>Loading products...</p>;

return (
  <div className="product-bar">
    {filteredProducts.map(product => (
      <div key={product.sku} className="product-card">
        <img src={product.image_url} alt={product.name} className="product-image" />
        <div className="product-info">
          <h4>{product.name}</h4>
          <p>${parseFloat(product.price).toFixed(2)}</p>
          <button onClick={() => addToCart(product)}>Add to Cart</button>
        </div>
      </div>
    ))}
  </div>
);
};


export default ProductBar;