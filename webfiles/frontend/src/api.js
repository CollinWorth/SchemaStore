import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // this is if fast api is running on local host

export const loginUser = async (username, password) => {
    const response = await axios.post(`${API_URL}/login/`, {
        username,
        password,
    });
    return response.data;
};

export const createUser = async (username, password, email) => {
    const response = await axios.post(`${API_URL}/register/`, {
        username,
        password,
        email,
        role: "customer", 
    });
    return response.data;
};