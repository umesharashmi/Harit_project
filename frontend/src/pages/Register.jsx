import React, { useState } from "react";
import { registerUser } from "../api/api";
import "../styles/auth.css";

function Register() {
  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [error, setError] = useState("");

  const handleRegister = async () => {
    setError("");

    // 🔥 VALIDATION
    if (!form.username.trim()) {
      setError("Username is required");
      return;
    }

    if (form.username.length < 3) {
      setError("Username must be at least 3 characters");
      return;
    }

    if (!form.password) {
      setError("Password is required");
      return;
    }

    if (form.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    try {
      const res = await registerUser(form);
      alert(res.message);
      window.location.href = "/";
    } catch (err) {
      setError("Register failed (server error)");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Register</h2>

        {/* ERROR MESSAGE */}
        {error && <p className="error-text">{error}</p>}

        <input
          placeholder="Username"
          onChange={(e) =>
            setForm({ ...form, username: e.target.value })
          }
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
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