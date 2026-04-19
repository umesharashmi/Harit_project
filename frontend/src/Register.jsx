import React, { useState } from "react";
import { registerUser } from "./api/api";
import "./styles/auth.css";

function Register() {
  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const handleRegister = async () => {
    try {
      const res = await registerUser(form);
      alert(res.message);
      window.location.href = "/";
    } catch (err) {
      alert("Register failed");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Register</h2>

        <input
          placeholder="Username"
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button onClick={handleRegister}>Register</button>

        <span
          className="auth-link"
          onClick={() => (window.location.href = "/")}
        >
          Back to Login
        </span>
      </div>
    </div>
  );
}

export default Register;