import axios from 'axios';
import './styles/cart.css'
import { useCallback, useEffect, useState } from "react"
import { useCart } from './components/Cartcomp';
import { useNavigate } from 'react-router-dom';

function Payment(){
    return(
        <div className='cart-page'>
            <h2>Thank you for your purchase!</h2>
            <p>Your items should arrive in 100 years, we appreciate your business.</p>
            <p>We will send you an email when your items are shipped.</p>
            <p>Have a great day!</p>
            <p>Click <a href="/">here</a> to return to the home page.</p>
        </div>
    )
} export default Payment;