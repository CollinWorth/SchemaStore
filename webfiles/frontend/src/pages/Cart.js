import { useCart } from './components/Cartcomp';

const Cart = () => {
  const { cartItems, removeFromCart, updateQuantity } = useCart();

  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div>
      <h2>Your Cart</h2>
      {cartItems.length === 0 && <p>Cart is empty</p>}
      {cartItems.map(item => (
        <div key={item.id}>
          <h4>{item.name}</h4>
          <p>Price: ${item.price}</p>
          <p>Qty: {item.quantity}</p>
          <button onClick={() => updateQuantity(item.id, -1)}>-</button>
          <button onClick={() => updateQuantity(item.id, 1)}>+</button>
          <button onClick={() => removeFromCart(item.id)}>Remove</button>
        </div>
      ))}
      <h3>Total: ${total.toFixed(2)}</h3>
      <button disabled={cartItems.length === 0}>Checkout</button>
    </div>
  );
};

export default Cart;
