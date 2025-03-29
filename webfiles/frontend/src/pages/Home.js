import "./styles/home.css";
import React from "react";
import ProductBar from "./components/ProductBar"; 

function Home(){
    return(
        <div className="main-div">
            <h1>Welcome to Schema Store</h1>
            <h2 className="prod-list-lable">Suggested for you</h2>   
            <ProductBar/>
            <h2 className="prod-list-lable">Huge Deals</h2>
            <ProductBar category="shoes"/>
        </div>
    );
}

export default Home;