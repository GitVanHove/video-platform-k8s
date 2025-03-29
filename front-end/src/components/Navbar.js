import { Link } from "react-router-dom";
import "../styles/NavBar.css";

const Navbar = () => (
  <nav className="navbar">
    <Link to="/">Home</Link>
    <Link to="/upload">Upload</Link>
    <Link to="/login">Login</Link>
  </nav>
);

export default Navbar;