import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/LoginPage.css";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const response = await fetch("", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      alert("Login successful!");
      navigate("/");
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="login-container">
      <h1 className="login-title">Login</h1>
      <input type="email" className="login-input" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" className="login-input" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button className="login-btn" onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginPage;