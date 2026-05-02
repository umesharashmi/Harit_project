import { useEffect } from "react";
import Navbar from "../component/Navbar";
import MainDashboard from "./MainDashboard";

export default function AdminDashboard() {

  useEffect(() => {
    const role = localStorage.getItem("role");

    if (role !== "admin") {
      window.location.href = "/";
    }
  }, []);

  return (
    <div>
      <Navbar />

      <h2 style={{ padding: "10px", color: "red" }}>
        🔥 Admin Panel
      </h2>

      <MainDashboard />
    </div>
  );
}