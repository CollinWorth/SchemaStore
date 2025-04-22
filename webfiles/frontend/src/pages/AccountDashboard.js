import {useState, useEffect} from 'react';
import axios from "axios";
import "./components/sidebar.css";
import { useNavigate } from "react-router-dom";


function AccountDashboard(){
    const username = sessionStorage.getItem("username");
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState("dash");
    const [users, setUsers] = useState([]);

    const handleLogout = () =>{
        sessionStorage.removeItem("username");
        navigate('/');
        window.location.reload();
    }

    const fetchUsers = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:8000/user/");
          const usersWithRoles = response.data.map(user => ({
            ...user,
            
          }));
          setUsers(usersWithRoles);
        } catch (err) {
          console.error("Failed to fetch users", err);
          setUsers([]);
        }
      };

        useEffect(() => {
          fetchUsers();
        }, []);

    return(
        <div className='userdash-container'>
            <div className="sidebar">
                <h2 onClick={() =>setActiveTab("dash")}>Hello {username}</h2>
                <ul>
                    <li><a onClick={() =>setActiveTab("orders")}>View Orders</a></li>
                    <li><a onClick={() =>setActiveTab("userInfo")}>User Information</a></li>
                    <li><a onClick={handleLogout}>Logout</a></li>
                </ul>
            </div>

            <main className='dashboard-content'>
                {activeTab === "dash" && (
                    <h1>Welcome To Your Account</h1>
                )}
                {activeTab === "orders" && (
                    <h1>Here are your recent orders</h1>
                )}
                {activeTab === "userInfo" && (
                    <table className="user-table">
                    <thead>
                      <tr>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.filter(user => user.username === sessionStorage.getItem("username")).map((user, index) => (
                        <tr key={index}>
                          <td>{user.username}</td>
                          <td>{user.email}</td>
                          <td>{user.role}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
                </main>                                                
        </div>

    )
}

export default AccountDashboard;