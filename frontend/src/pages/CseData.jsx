import { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import Navbar from "../component/Navbar";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const BASE_URL = process.env.REACT_APP_API_URL;

export default function CseData() {
  const [filters, setFilters] = useState({});
  const [chartData, setChartData] = useState(null);
  const [selected, setSelected] = useState({
    company: "",
    industry: "",
    board: "",
  });

  // LOAD FILTERS
  useEffect(() => {
    axios.get(`${BASE_URL}/equity/filters`)
      .then((res) => setFilters(res.data))
      .catch((err) => console.log(err));

    loadChart();
  }, []);

  // LOAD CHART DATA
  const loadChart = (params = {}) => {
    axios
      .get(`${BASE_URL}/equity/chart`, { params })
      .then((res) => {
        setChartData({
          labels: res.data.labels,
          datasets: [
            {
              label: "Avg Close Price",
              data: res.data.avg_price,
              borderColor: "blue",
              tension: 0.3,
            },
            {
              label: "Turnover",
              data: res.data.turnover,
              borderColor: "green",
              tension: 0.3,
            },
          ],
        });
      })
      .catch((err) => console.log(err));
  };

  // APPLY FILTER
  const handleFilter = () => {
    loadChart(selected);
  };

  return (
    <div style={{ padding: "20px" }}>
        <Navbar />
      <h2>📊 CSE Data Dashboard</h2>

      {/* FILTER SECTION */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>

        {/* Company */}
        <select
          onChange={(e) => setSelected({ ...selected, company: e.target.value })}
        >
          <option value="">All Companies</option>
          {filters.companies?.map((c, i) => (
            <option key={i} value={c}>{c}</option>
          ))}
        </select>

        {/* Industry */}
        <select
          onChange={(e) => setSelected({ ...selected, industry: e.target.value })}
        >
          <option value="">All Industries</option>
          {filters.industries?.map((i, idx) => (
            <option key={idx} value={i}>{i}</option>
          ))}
        </select>

        {/* Board */}
        <select
          onChange={(e) => setSelected({ ...selected, board: e.target.value })}
        >
          <option value="">All Boards</option>
          {filters.boards?.map((b, idx) => (
            <option key={idx} value={b}>{b}</option>
          ))}
        </select>

        <button onClick={handleFilter}>
          Apply Filters
        </button>
      </div>

      {/* CHART */}
      <div style={{ width: "100%", height: "420px" }}>
        {chartData ? (
          <Line data={chartData} />
        ) : (
          <p>Loading chart...</p>
        )}
      </div>
    </div>
  );
}