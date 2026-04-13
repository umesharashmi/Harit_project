import { useEffect, useState } from "react";
import { getFilters, getAvg, getRange } from "./api";
import "./styles.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default function Dashboard() {

  const [filters, setFilters] = useState({
    dates: [],
    items: [],
    categories: [],
    cities: []
  });

  const [form, setForm] = useState({
    date: "",
    item: "",
    category: "",
    city: "",
    start: "",
    end: ""
  });

  const [mode, setMode] = useState("single");
  const [avg, setAvg] = useState(null);
  const [results, setResults] = useState([]);
  const [chartData, setChartData] = useState([]);

  // LOAD FILTERS
  useEffect(() => {
    getFilters()
      .then(res => {
        setFilters({
          dates: res.data.dates || [],
          items: res.data.items || [],
          categories: res.data.categories || [],
          cities: res.data.cities || []
        });
      })
      .catch(err => console.log(err));
  }, []);

  // FILTER ITEMS
  const filteredItems = filters.items.filter(
    (i) => i.category === form.category
  );

  const filteredDates = filters.dates;

  // SINGLE SEARCH
  const search = async () => {
    if (!form.date || !form.item || !form.category || !form.city) {
      alert("Fill all fields");
      return;
    }

    const res = await getAvg({
      date: form.date,
      item: form.item,
      category: form.category,
      city: form.city
    });

    const value = res.data.average ?? 0;

    setAvg(value);
    setResults([{
      type: "Single",
      date: form.date,
      item: form.item,
      category: form.category,
      city: form.city,
      average: value
    }]);

    setChartData([]);
  };

  // RANGE SEARCH
  const rangeSearch = async () => {
    if (!form.start || !form.end || !form.item || !form.category || !form.city) {
      alert("Fill all fields");
      return;
    }

    const res = await getRange({
      start: form.start,
      end: form.end,
      item: form.item,
      category: form.category,
      city: form.city
    });

    const value = res.data.average ?? 0;

    setAvg(value);

    setResults([{
      type: "Range",
      date: `${form.start} → ${form.end}`,
      item: form.item,
      category: form.category,
      city: form.city,
      average: value
    }]);

    const rawData = res.data.daily || res.data.data || [];

    const formattedData = rawData.map(d => ({
      date: d.date ? d.date : d.day,
      average: d.average !== undefined ? d.average : d.avg
    }));

    setChartData(formattedData);
  };

  // ✅ EXPORT TO EXCEL (FIXED)
  const exportToExcel = () => {
    if (chartData.length === 0) {
      alert("No data to export");
      return;
    }

    const exportData = chartData.map(d => ({
      date: d.date,
      average: d.average,
      item: form.item,
      category: form.category,
      city: form.city
    }));

    const worksheet = XLSX.utils.json_to_sheet(exportData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Prices");

    const excelBuffer = XLSX.write(workbook, {
      bookType: "xlsx",
      type: "array"
    });

    const file = new Blob([excelBuffer], {
      type:
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    });

    saveAs(file, "price_data.xlsx");
  };

  return (
    <div className="container">

      <h1 className="title">Price Dashboard</h1>
      <hr />

      {/* MODE */}
      <div className="mode-buttons">
        <button
          className={mode === "single" ? "active" : ""}
          onClick={() => setMode("single")}
        >
          Single Date
        </button>

        <button
          className={mode === "range" ? "active" : ""}
          onClick={() => setMode("range")}
        >
          Date Range
        </button>
      </div>

      <hr />

      {/* FILTERS */}
      <div className="card">

        <select
          value={form.category}
          onChange={e =>
            setForm({ ...form, category: e.target.value, item: "", date: "", start: "", end: "" })
          }
        >
          <option value="">Category</option>
          {filters.categories.map(c => (
            <option key={c}>{c}</option>
          ))}
        </select>

        <select
          value={form.item}
          disabled={!form.category}
          onChange={e => setForm({...form, item: e.target.value, date: "", start: "", end: ""})}
        >
          <option value="">Item</option>
          {filteredItems.map(i => (
            <option key={i.name} value={i.name}>
              {i.name}
            </option>
          ))}
        </select>

        <select
          value={form.city}
          onChange={e => setForm({...form, city: e.target.value, date: "", start: "", end: ""})}
        >
          <option value="">City</option>
          {filters.cities.map(c => (
            <option key={c}>{c}</option>
          ))}
        </select>

      </div>

      {/* SINGLE */}
      {mode === "single" && (
        <div className="card">

          <select
            value={form.date}
            disabled={!form.item || !form.category || !form.city}
            onChange={e => setForm({...form, date: e.target.value})}
          >
            <option value="">Select Date</option>
            {filteredDates.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>

          <button className="search-btn" onClick={search}>
            🔍 Get Average
          </button>

        </div>
      )}

      {/* RANGE */}
      {mode === "range" && (
        <div className="card">

          <select
            value={form.start}
            disabled={!form.item || !form.category || !form.city}
            onChange={e => setForm({...form, start: e.target.value})}
          >
            <option value="">Start Date</option>
            {filteredDates.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>

          <select
            value={form.end}
            disabled={!form.item || !form.category || !form.city}
            onChange={e => setForm({...form, end: e.target.value})}
          >
            <option value="">End Date</option>
            {filteredDates.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>

          <button className="search-btn" onClick={rangeSearch}>
            🔍 Get Range Average
          </button>

        </div>
      )}

      {/* AVG */}
      {avg !== null && (
        <div className="avg-card">
          💰 Average Price: {Number(avg).toFixed(2)}
        </div>
      )}

      {/* CHART */}
      {chartData.length > 0 && (
        <div className="card">
          <h3>📊 Price Trend</h3>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="average" />
            </LineChart>
          </ResponsiveContainer>

          <button className="search-btn" onClick={exportToExcel}>
            ⬇ Export to Excel
          </button>
        </div>
      )}

      {/* TABLE */}
      {results.length > 0 && (
        <table className="table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Date</th>
              <th>Item</th>
              <th>Category</th>
              <th>City</th>
              <th>Avg</th>
            </tr>
          </thead>

          <tbody>
            {results.map((r, i) => (
              <tr key={i}>
                <td>{r.type}</td>
                <td>{r.date}</td>
                <td>{r.item}</td>
                <td>{r.category}</td>
                <td>{r.city}</td>
                <td>{Number(r.average).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

    </div>
  );
}