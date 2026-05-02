import { useEffect } from "react";
import Navbar from "../component/Navbar";
import MainDashboard from "./MainDashboard";

export default function ViewDashboard() {

  useEffect(() => {
    const role = localStorage.getItem("role");

    if (role !== "viewer") {
      window.location.href = "/";
    }
  }, []);

  return (
    <div>
      <Navbar />
      
            <h2 style={{ padding: "10px", color: "red" }}>
              🔥 Welcome to Viewer Panel
            </h2>
      
            <MainDashboard />
    </div>
  );
}