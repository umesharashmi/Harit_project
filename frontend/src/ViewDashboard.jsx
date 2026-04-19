import { useEffect } from "react";
import Dashboard from "./Dashboard";

export default function ViewDashboard() {

  useEffect(() => {
    const role = localStorage.getItem("role");

    if (role !== "viewer") {
      window.location.href = "/";
    }
  }, []);

  return <Dashboard hideDownload={true} />;
}