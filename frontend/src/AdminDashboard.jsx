import { useEffect } from "react";
import Dashboard from "./Dashboard";

export default function AdminDashboard() {

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    if (role !== "admin") {
      window.location.href = "/";
    }
  }, []);

  return <Dashboard hideDownload={false} />;
}