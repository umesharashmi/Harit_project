import Navbar from "../component/Navbar";
import "../styles/tourism.css";
import { useEffect, useState } from "react";

import {
  getCountryFilters,
  getCountryArrivals
} from "../api/api";

export default function CountryArrival() {

  const [filters, setFilters] = useState({
    countries: [],
    years: [],
    months: []
  });

  const [year, setYear] = useState("");
  const [country, setCountry] = useState("");
  const [month, setMonth] = useState("");

  const [data, setData] = useState([]);
  const [compareMode, setCompareMode] = useState(false);

  // LOAD FILTERS
  useEffect(() => {
    getCountryFilters()
      .then((res) => setFilters(res))
      .catch(() =>
        setFilters({
          countries: [],
          years: [],
          months: []
        })
      );
  }, []);

  // NORMAL SEARCH
  const search = () => {
    setCompareMode(false);

    if (!year) return;

    getCountryArrivals({
      year: Number(year),
      country,
      month
    })
      .then((res) => setData(res))
      .catch((err) => console.log(err));
  };

  const loadCompare = () => {
  getCountryArrivals({
    country,
    month: ""
  })
    .then((res) => {
      setData(res);
      setCompareMode(true);
    })
    .catch((err) => console.log(err));
};

  return (
    <div className="tourism-container">

      <Navbar />

      <h2 className="tourism-title">
        {compareMode
          ? "Country Comparison (2025 - 2026)"
          : "Country Arrival Report"}
      </h2>

      {/* FILTER BOX */}
      <div className="filters-box">

        <select onChange={(e) => setYear(e.target.value)}>
          <option value="">Select Year</option>
          {(filters.years || []).map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>

        <select onChange={(e) => setCountry(e.target.value)}>
          <option value="">All Countries</option>
          {(filters.countries || []).map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <select onChange={(e) => setMonth(e.target.value)}>
          <option value="">Total</option>
          {(filters.months || []).map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>

        <button className="search-btn" onClick={search}>
          🔍 Search
        </button>

        <button className="search-btn" onClick={loadCompare}>
          📊 Compare
        </button>

      </div>

      {/* TABLE */}
      <table className="tourism-table">

        <thead>
          <tr>
            <th>Country</th>
            <th>Year</th>
            <th>Month</th>
            <th>Count</th>
          </tr>
        </thead>

        <tbody>
          {data.length > 0 ? (
            data.map((d, i) => (
              <tr key={i}>
                <td>{d.country}</td>
                <td>{d.year}</td>
                <td>{d.month || "total"}</td>
                <td>{d.count}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="no-data">
                No Data Found
              </td>
            </tr>
          )}
        </tbody>

      </table>

    </div>
  );
}