import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

// 🔐 JWT TOKEN HEADER FUNCTION
const getAuthHeader = () => {
  const token = localStorage.getItem("token");

  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };
};

// FILTERS (Protected)
export const getFilters = () =>
  axios.get(`${BASE_URL}/filters`, getAuthHeader());

// SINGLE AVG (Protected)
export const getAvg = (params) =>
  axios.get(`${BASE_URL}/avg`, {
    params,
    ...getAuthHeader()
  });

// RANGE AVG (Protected)
export const getRange = (params) =>
  axios.get(`${BASE_URL}/avg-range`, {
    params,
    ...getAuthHeader()
  });

// ✅ REGISTER (NO TOKEN NEEDED)
export const registerUser = async (data) => {
  const res = await axios.post(`${BASE_URL}/register`, data);
  return res.data;
};

// ✅ LOGIN (NO TOKEN NEEDED)
export const loginUser = async (data) => {
  const res = await axios.post(`${BASE_URL}/login`, data);

  // 🔥 TOKEN SAVE (IMPORTANT)
  localStorage.setItem("token", res.data.access_token);
  localStorage.setItem("role", res.data.role);

  return res.data;
};