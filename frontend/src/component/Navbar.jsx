import { Link, useNavigate, useLocation } from "react-router-dom";
import "../styles/navbar.css";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = localStorage.getItem("role");

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="navbar">

      <h2 className="logo">System</h2>

      <div className="nav-links">

        <Link
          to={role === "admin" ? "/admin" : role === "viewer" ? "/viewer" : "/dashboard"}
          className={`nav-link ${isActive("/dashboard") ? "active" : ""}`}
        >
          🏠 Home
        </Link>

        <Link
          to="/tourism"
          className={`nav-link ${isActive("/tourism") ? "active" : ""}`}
        >
          🌍 Tourism
        </Link>

        <Link
          to="/vegetable"
          className={`nav-link ${isActive("/vegetable") ? "active" : ""}`}
        >
          🥦 Vegetable
        </Link>

        <Link
          to="/cse"
           className={`nav-link ${isActive("/cse") ? "active" : ""}`}
            >
            📈 CSE Data
              </Link>

        <button onClick={logout} className="logout-btn">
          Logout
        </button>

      </div>
    </div>
  );
}