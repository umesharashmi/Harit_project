import { useEffect } from "react";
import Navbar from "../component/Navbar";
import Dashboard from "./Dashboard";

export default function Vegetable() {

  const role = localStorage.getItem("role");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/";
    }
  }, []);

  return (
    <div>
      <Navbar />

      <div style={{ padding: "10px" }}>
        <h2>🥦 Vegetable Price Data</h2>
      </div>

      {/* ROLE BASED DASHBOARD */}
      <Dashboard hideDownload={role !== "admin"} />
    </div>
  );
}