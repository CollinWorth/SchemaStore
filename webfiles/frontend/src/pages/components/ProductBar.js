import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ProductBar.css";
import { useCart } from './Cartcomp';

import sneakers from "../assets/sneakers.jpg";
import joggers from "../assets/joggers.jpg";
import sweatshirt from "../assets/sweatshirt.jpg"
import sunglasses from "../assets/sunglasses.jpg"

const products = [ //Place holder for items, so that we have some images
  {id: 1, name: "Sneakers", price: "79.99", image: sneakers},
  {id: 2, name: "Joggers", price: "49.99", image: joggers},
  {id: 3, name: "Sweatshirt", price: "59.99", image: sweatshirt},
  {id: 4, name: "Sunglasses", price: "39.99", image: sunglasses},
]

const ProductBar = () => {
  /*const [products, setProducts] = useState([]);  This will be implemented once the product db is done

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/products")
      .then((response) => setProducts(response.data))
      .catch((error) => console.error("Error fetching products:", error));
  }, []);*/

const {addToCart} = useCart();

  return (
    <div className="product-bar">
      {products.map((product) => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.name} className="product-image" />
          <div className="product-info">
            <h4>{product.name}</h4>
            <p>${product.price}</p>
            <button onClick={() => addToCart(product)}>Add to Cart</button>
          </div>
        </div>
      ))}
    </div>
  );
}

   /*  {products.map((product) => (
  <div key={product.id} className="product-card">
    <img src={product.image_url} alt={product.name} className="product-image" />
    <div className="product-info">
      <h4>{product.name}</h4>
      <p>${product.price.toFixed(2)}</p>
    </div>
  </div>
))}*/


export default ProductBar;