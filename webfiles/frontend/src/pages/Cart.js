import axios from 'axios';
import './styles/cart.css'
import { useCallback, useEffect, useState } from "react"
import { useCart } from './components/Cartcomp';
import { useNavigate } from 'react-router-dom';

const Cart = () => {

  const { cart, addToCart, removeFromCart, fetchCart } = useCart();
  const navigate = useNavigate();
  const [product_list, setList] = useState(new Map());
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchCart();
  },[]);

  const handleCheckout = () => {
    navigate('/payment');
  };

  const newMap = new Map();

  const fetchItems = async () =>{
    console.log("cart: ",cart);
    var newtotal = 0;
    for (let sku in cart){
      const res = await axios.get(`http://127.0.0.1:8000/products/${sku}`);
      newMap.set(sku,res.data);
      newtotal += cart[sku]*res.data.price;
      console.log(res);
    }
    setList(newMap);
    setTotal(newtotal);
  };


  useEffect(() => {
    if (Object.keys(cart).length > 0) {
      fetchItems();
    }
    else {
      setTotal(0);
    }
  }, [cart]);

  return (
    <div className='cart-page'>
      <h2>Your Cart</h2>
      {Object.keys(cart).length === 0 && <p>Cart is empty</p>}

      {Object.entries(cart).map(([sku, quantity]) => {
        const product = product_list.get(sku);
        if (!product) return null;

        return (
          <div key={sku} className='cart-item'>
            <img 
              src={product.img} 
              alt={product.name} 
              className="cart-img" 
            />
            <div className='item-details'>
              <h4>{product.name}</h4>
              <p>Price: ${product.price}</p>
              <div className="qty-row">
                <p>Qty: {quantity}</p>
                <div className="item-controls">
                  <button onClick={() => removeFromCart(sku)}>-</button>
                  <button onClick={() => addToCart(sku)}>+</button>
                  <button onClick={() => removeFromCart(sku, cart[sku])}>Remove</button>
                </div>
              </div>
            </div>
          </div>
        );
      })}

      <h3>Total: ${total.toFixed(2)}</h3>
      <button 
        className='checkout' 
        disabled={Object.keys(cart).length === 0}
        onClick={handleCheckout}
      >
        Checkout
      </button>
    </div>
  );
};

export default Cart;