import "./components/sidebar.css";
import { useNavigate } from "react-router-dom";


function AccountDashboard(){
    const username = sessionStorage.getItem("username");
    const navigate = useNavigate();

    const handleLogout = () =>{
        sessionStorage.removeItem("username");
        navigate('/');
        window.location.reload();
    }

    return(
        <div>
            <h1>Welcome To Your Account</h1>
            <div className="sidebar">
                <h2>Hello {username}</h2>
                <ul>
                    <li><a href="/">View Orders</a></li>
                    <li><a href="/">Update Contact Information</a></li>
                    <li><a onClick={handleLogout}>Logout</a></li>
                </ul>
            </div>                                                
        </div>
    )
}

export default AccountDashboard;