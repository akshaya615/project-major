import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Register.css";

function Register() {
  const navigate = useNavigate();
  const [role, setRole] = useState("user");

  return (
    <div className="register-container">
      <div className="register-card">
        <h2>{role === "user" ? "User Registration" : "Admin Registration"}</h2>

        {/* ROLE TOGGLE */}
        <div className="role-toggle">
          <button
            className={role === "user" ? "active" : ""}
            onClick={() => setRole("user")}
          >
            User
          </button>
          <button
            className={role === "admin" ? "active" : ""}
            onClick={() => setRole("admin")}
          >
            Admin
          </button>
        </div>

        {/* FORM */}
        <input type="text" placeholder="Full Name" />
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <input type="password" placeholder="Confirm Password" />

        <button className="register-btn">Register</button>

        <p className="login-text">
          Already registered?{" "}
          <span onClick={() => navigate("/login")}>Login</span>
        </p>
      </div>
    </div>
  );
}

export default Register;