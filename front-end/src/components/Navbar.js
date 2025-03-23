import { Link } from "react-router-dom";

const Navbar = () => (
  <nav>
    <Link to="/">Home</Link> | 
    <Link to="/upload">Upload</Link> | 
    <Link to="/login">Login</Link>
  </nav>
);

export default Navbar;