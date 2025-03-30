import { Link , useNavigate } from "react-router-dom";
import "../styles/NavBar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  const handleLogout = () => {
    localStorage.removeItem("user_id"); // Clear user_id
    alert("Logged out successfully!");
    navigate("/login"); // Redirect to login page
  };

  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <Link to="/upload">Upload</Link>
      {!userId ? (
        <Link to="/login">Login</Link>
      ) : (
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      )}
    </nav>
  );
};
export default Navbar;