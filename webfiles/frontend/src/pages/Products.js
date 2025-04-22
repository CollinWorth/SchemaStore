import React, { useEffect, useState } from "react";
import axios from "axios";
import "./styles/products.css";
import { useCart } from './components/Cartcomp';

const ProductPage = () => {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [allCategories, setAllCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart, fetchCart } = useCart();

  //expand card
  const [expandedCard, setExpandedCard] = useState(null);

  const toggleExpand = (sku) => {
    setExpandedCard((prev) => (prev === sku ? null : sku));
  };
  

  // Fetch all products
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/products/");
      setProducts(response.data);
    } catch (err) {
      console.error("Failed to fetch products", err);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  // Search products
  const searchProducts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/products/search?query=${search}`);
      setProducts(response.data);
    } catch (err) {
      console.error("Search failed", err);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  // Category-based filter (local, client-side)
  const filterByCategory = () => {
    if (!categoryFilter) return products;
    return products.filter((product) =>
      product.categories.includes(categoryFilter)
    );
  };

  // Get all unique categories from products (optional pre-filtering)
  const extractCategories = (productList) => {
    const catSet = new Set();
    productList.forEach(p => {
      if (Array.isArray(p.categories)) {
        p.categories.forEach(c => catSet.add(c));
      }
    });
    setAllCategories([...catSet]);
  };

  // Effects
  useEffect(() => {
    fetchProducts();
    fetchCart();
  }, []);

  useEffect(() => {
    extractCategories(products);
  }, [products]);

  const displayedProducts = filterByCategory();

  return (
    <div className="product-page">
      <h1>All Products</h1>

      {/* Filters */}
      <div className="filters">
        <input
          type="text"
          placeholder="Search by name or description..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button onClick={searchProducts}>Search</button>

        <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)}>
          <option value="">All Categories</option>
          {allCategories.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {/* Product Grid */}
      {loading ? (
        <p>Loading products...</p>
      ) : (
        <div className="product-grid">
          {displayedProducts.length === 0 ? (
            <p>No products found.</p>
          ) : (
            displayedProducts.map((product) => (
                <div
                key={product.sku}
                className={`product-card ${expandedCard === product.sku ? "expanded" : ""}`}
                onClick={() => toggleExpand(product.sku)}
                >
                <img src={product.img} alt={product.name} />
                <h3>{product.name}</h3>

                <div className="product-price">${product.price.toFixed(2)}</div>

                    {expandedCard === product.sku && (
                        <div className="product-popout" onClick={(e) => e.stopPropagation()}>
                            <p><strong>Description:</strong> {product.description}</p>
                            <p><strong>Stock:</strong> {product.stock}</p>
                            <div className="categories">
                                {(product.categories ?? []).map((cat) => (
                                <span key={cat} className="category-tag">{cat}</span>
                                ))}
                            </div>
                            <button
                                className="add-to-cart"
                                onClick={(e) => {
                                e.stopPropagation();
                                console.log("Add to cart:", product.sku);
                                addToCart(product.sku, 1);
                                }}
                            >
                                Add to Cart
                            </button>
                        </div>
                    )}
                </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default ProductPage;
