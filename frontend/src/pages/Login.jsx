import { useState } from "react";
import { loginUser } from "../api/api";
import Navbar from "../component/Navbar";
import "../styles/auth.css";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  
const handleLogin = async () => {
  try {
    const res = await loginUser(form);

    localStorage.setItem("token", res.access_token);
    localStorage.setItem("role", res.role);

    if (res.role === "admin") {
      window.location.href = "/admin";
    } else {
      window.location.href = "/viewer";
    }

  } catch (err) {
    alert("Login failed");
  }
};

  return (
    
    
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>

        <input
          placeholder="Username"
          onChange={(e)=>setForm({...form, username:e.target.value})}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e)=>setForm({...form, password:e.target.value})}
        />

        <button onClick={handleLogin}>Login</button>

        <span
          className="auth-link"
          onClick={() => (window.location.href = "/register")}
        >
          Create account
        </span>
      </div>
    </div>
  );
}