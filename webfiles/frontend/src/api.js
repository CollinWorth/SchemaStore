import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // this is if fast api is running on local host

export const loginUser = async (username, password) => {
    const response = await axios.post(`${API_URL}/login/`, {
        username,
        password,
    });
    return response.data;
};

export const createUser = async (username, password, email, role_id) => {
    const response = await axios.post(`${API_URL}/register/`, {
        username,
        password,
        email,
        role_id, 
    });
    return response.data;
};

// Fetch all products
export const getProducts = async () => {
    try {
        const response = await axios.get(`${API_URL}/products/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching products:", error);
        throw error;
    }
};

// Fetch a single product by SKU
export const getProductBySku = async (sku) => {
    try {
        const response = await axios.get(`${API_URL}/products/${sku}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching product with SKU ${sku}:`, error);
        throw error;
    }
};

// Add a new product
export const addProduct = async (productData) => {
    try {
        const response = await axios.post(`${API_URL}/products/`, productData);
        return response.data;
    } catch (error) {
        console.error("Error adding product:", error);
        throw error;
    }
};

// Delete a product by SKU
export const deleteProduct = async (sku) => {
    try {
        const response = await axios.delete(`${API_URL}/products/${sku}`);
        return response.data;
    } catch (error) {
        console.error(`Error deleting product with SKU ${sku}:`, error);
        throw error;
    }
};