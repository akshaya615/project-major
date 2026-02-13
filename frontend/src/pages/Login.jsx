import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const [role, setRole] = useState("user");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    role === "user"
      ? navigate("/user-dashboard")
      : navigate("/admin-dashboard");
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>

        <div className="toggle">
          <button
            className={role === "user" ? "active" : ""}
            onClick={() => setRole("user")}
            type="button"
          >
            User
          </button>
          <button
            className={role === "admin" ? "active" : ""}
            onClick={() => setRole("admin")}
            type="button"
          >
            Admin
          </button>
        </div>

        <form className="login-form" onSubmit={handleLogin}>
          <input type="email" placeholder="Email" required />
          <input type="password" placeholder="Password" required />
          <button type="submit">Login as {role}</button>
        </form>

        <p className="register-text">
          Not yet registered?{" "}
          <span
            style={{ color: "#2563eb", cursor: "pointer" }}
            onClick={() => navigate("/register")}
          >
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

export default Login;
