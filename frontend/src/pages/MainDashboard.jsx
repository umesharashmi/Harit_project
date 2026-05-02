
import "../styles/dashboard.css";

export default function MainDashboard() {
  return (
    <div className="dashboard-container">

     

      <div className="dashboard-content">

        <h2 className="dashboard-title">Welcome Dashboard</h2>

        <p className="dashboard-text">
          Select menu from navbar:
        </p>

        <ul className="dashboard-list">
          <li>Tourism Data</li>
          <li>Vegetable Price Data</li>
        </ul>

      </div>
    </div>
  );
}