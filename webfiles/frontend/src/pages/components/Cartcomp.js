import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
  const username = sessionStorage.getItem("username");

  const [cart, setCart] = useState({}); // { sku: quantity }


  if (username === "undefined") {
    console.warn("No username in sessionStorage — cart requests may fail");
    return;
  }

  const fetchCart = async () => {
    const res = await axios.get(`http://127.0.0.1:8000/cart/?username=${username}`);
    setCart(res.data.products);
  };



  const addToCart = async (sku, amount = 1) => {
    try{
      await axios.post("http://127.0.0.1:8000/cart/", {
      username,
      product_sku: sku,
      amount
    });
  } catch (err){
    console.error("Cart Error:", err.response?.data || err.message);
  }
    fetchCart(); // Refresh local cart
  };

  const removeFromCart = async (sku, amount = 1) => {
    await axios.delete("http://127.0.0.1:8000/cart/", {
      data: {
        username,
        product_sku: sku,
        amount
      }
    });
    fetchCart();
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, fetchCart }}>
      {children}
    </CartContext.Provider>
  );
};
