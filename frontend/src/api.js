import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

// FILTERS
export const getFilters = () =>
  axios.get(`${BASE_URL}/filters`);

//  SINGLE AVG
export const getAvg = (params) =>
  axios.get(`${BASE_URL}/avg`, { params });

// RANGE AVG
export const getRange = (params) =>
  axios.get(`${BASE_URL}/avg-range`, { params });