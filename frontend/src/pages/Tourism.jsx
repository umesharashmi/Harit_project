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

  // LOAD FILTERS
  useEffect(() => {
    getCountryFilters()
      .then((res) => {
        setFilters(res?.data || {
          countries: [],
          years: [],
          months: []
        });
      })
      .catch((err) => {
        console.log("FILTER ERROR:", err);
        setFilters({
          countries: [],
          years: [],
          months: []
        });
      });
  }, []);

  // SEARCH
  const search = () => {
    if (!year) return; // prevent 422 error

    getCountryArrivals({
      year: Number(year),
      country,
      month
    })
      .then((res) => {
        setData(res || []);
      })
      .catch((err) => console.log("SEARCH ERROR:", err));
  };

  return (
    <div className="tourism-container">

      <Navbar />

      <h2 className="tourism-title">Country Arrival Report</h2>

      {/* FILTERS */}
      <div className="tourism-filters">

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