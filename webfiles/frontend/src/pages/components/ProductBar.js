import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./ProductBar.css";
import { useCart } from './Cartcomp';
import { getProducts } from "../../api.js";


const ProductBar = () => { //{ overrideProducts, category}
  const { addToCart } = useCart();
  const productsRef = useRef([]); // Local "state" without using useState
  //const [products, setProducts] = useState([]);
  const [hasFetched, setHasFetched] = useState(false); // To trigger a rerender
  //const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const allProducts = await getProducts(); // fetch all products
        productsRef.current = allProducts;       // store in ref
        setHasFetched(true);                     // force re-render
      } catch (error) {
        console.error("Failed to load products", error);
      }
    };

    fetchProducts();
  }, []);

//const filteredProducts = overrideProducts 
//?overrideProducts
//:category
//? products.filter(p => p.category === category)
//: products;
//if (loading) return <p>Loading products...</p>;

return (
  <div className="product-bar">
    {productsRef.current.length === 0 && !hasFetched && <p>Loading products...</p>}
    {productsRef.current.map((product) => (
      <div key={product.sku} className="product-card">
        <img src={product.image} alt={product.name} className="product-image" />
        <div className="product-info">
          <h4>{product.name}</h4>
          <p>${parseFloat(product.price).toFixed(2)}</p>
          <button onClick={() => addToCart(product.sku, 1)}>Add to Cart</button>
        </div>
      </div>
    ))}
  </div>
);
};


export default ProductBar;