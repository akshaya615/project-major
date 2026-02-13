import { useState, useRef, useEffect } from "react";
import LiveMap from "../components/LiveMap";
import "../styles/theme.css";
import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {

  const [activeTab, setActiveTab] = useState("dashboard");

  /* 🔽 DROPDOWN STATE */
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  /* Close dropdown on outside click */
  useEffect(() => {
    const handler = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  /* Logout */
  const handleLogout = () => {
    navigate("/login");
  };

  return (
    <div className="dashboard admin">

      {/* ================= SIDEBAR ================= */}
      <div className="sidebar dark">
        <h2>AI Road Safety</h2>
        <ul>
          <li onClick={() => setActiveTab("dashboard")}>Dashboard</li>
          <li onClick={() => setActiveTab("hotspots")}>Hotspot Management</li>
          <li onClick={() => setActiveTab("reports")}>User Reports</li>
          <li>Admin Panel</li>
        </ul>
      </div>

      {/* ================= MAIN ================= */}
      <div className="main">

        {/* ================= TOPBAR ================= */}
        <div className="topbar dark">
          <h2>
            {activeTab === "dashboard" && "Dashboard"}
            {activeTab === "hotspots" && "Hotspot Management"}
            {activeTab === "reports" && "User Reports"}
          </h2>

          {/* 🔽 ADMIN DROPDOWN */}
          <div className="admin-profile" ref={dropdownRef}>

            <div
              className="profile-trigger"
              onClick={() => setOpen(!open)}
            >
              <div className="avatar">A</div>
              <span>Admin ⬇</span>
            </div>

            {open && (
              <div className="admin-dropdown">

                <div className="admin-info">
                  <div className="avatar large">A</div>
                  <div>
                    <strong>Admin</strong>
                    <p className="online">● Online</p>
                  </div>
                </div>

                <div className="dropdown-divider"></div>

                <div
                  className="dropdown-item logout"
                  onClick={handleLogout}
                >
                  🚪 Logout
                </div>

              </div>
            )}

          </div>
        </div>

        {/* ================= DASHBOARD ================= */}
        {activeTab === "dashboard" && (
          <>
            <div className="stats">
              <div className="card">
                Total Accidents<br /><b>56</b>
              </div>

              <div className="card high">
                High Severity<br /><b>12</b>
              </div>

              <div className="card medium">
                Hotspots<br /><b>8</b>
              </div>

              <div className="card safe">
                Safe Routes<br /><b>24</b>
              </div>
            </div>

            <div className="map-section">
              <h3>Hotspot Management</h3>
              <LiveMap />
            </div>
          </>
        )}

        {/* ================= HOTSPOTS ================= */}
        {activeTab === "hotspots" && (
          <>
            <div className="map-section">
              <LiveMap />
            </div>

            <div className="tables">
              <div>
                <h3>Accident Hotspots</h3>

                <table className="table">
                  <tr>
                    <th>Rank</th>
                    <th>Location</th>
                    <th>Severity</th>
                    <th>Total Accidents</th>
                  </tr>

                  <tr>
                    <td>1</td>
                    <td>MG Road</td>
                    <td className="high">High</td>
                    <td>42</td>
                  </tr>

                  <tr>
                    <td>2</td>
                    <td>Jayanagar</td>
                    <td className="medium">Medium</td>
                    <td>28</td>
                  </tr>

                  <tr>
                    <td>3</td>
                    <td>Sarjapur Road</td>
                    <td className="safe">Low</td>
                    <td>35</td>
                  </tr>
                </table>
              </div>
            </div>
          </>
        )}

        {/* ================= REPORTS ================= */}
        {activeTab === "reports" && (
          <div className="tables">
            <div>
              <h3>Recent Feedback</h3>

              <table className="table">
                <tr>
                  <th>User</th>
                  <th>Feedback</th>
                  <th>Submitted</th>
                </tr>

                <tr>
                  <td>John</td>
                  <td>Slippery road near MG Road</td>
                  <td>5 mins ago</td>
                </tr>

                <tr>
                  <td>user123</td>
                  <td>Traffic congestion in Jayanagar</td>
                  <td>20 mins ago</td>
                </tr>

                <tr>
                  <td>Sarah</td>
                  <td>Poor lighting near Hotspot #5</td>
                  <td>1 hr ago</td>
                </tr>
              </table>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
