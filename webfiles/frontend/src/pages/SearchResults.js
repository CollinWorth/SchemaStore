import { useSearchParams } from "react-router-dom";
import ProductBar from "./components/ProductBar"; // or wherever yours is
import products from "./data/products"; // import your data source

const SearchResults = () => {
  const [params] = useSearchParams();
  const query = params.get("query")?.toLowerCase() || "";
  const category = params.get("category") || "all";

  const filtered = products.filter((p) => {
    const matchesCategory = category === "all" || p.category === category;
    const matchesQuery = p.name.toLowerCase().includes(query);
    return matchesCategory && matchesQuery;
  });

  return (
    <div>
      <h2>Search Results</h2>
      {filtered.length === 0 ? (
        <p>No products found for "{query}" in category "{category}"</p>
      ) : (
        <ProductBar overrideProducts={filtered} />
      )}
    </div>
  );
};

export default SearchResults;
