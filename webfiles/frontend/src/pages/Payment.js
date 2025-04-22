import axios from 'axios';
import './styles/cart.css'
import { useCallback, useEffect, useState } from "react"
import { useCart } from './components/Cartcomp';
import { useNavigate } from 'react-router-dom';

function Payment(){
    return(
        <div className='cart-page'>
            <h2>Payment</h2>
            <p>Thank you for your purchase!</p>
        </div>
    )
} export default Payment;