import { Routes, Route } from "react-router-dom";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";

function App() {
  return (
    <Routes>
      {/* PUBLIC ROUTES */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* USER ROUTE */}
      <Route path="/user-dashboard" element={<UserDashboard />} />

      {/* ADMIN ROUTE */}
      <Route path="/admin-dashboard" element={<AdminDashboard />} />
    </Routes>
  );
}

export default App;