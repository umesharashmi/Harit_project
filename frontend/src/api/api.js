import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL;

//  JWT TOKEN HEADER FUNCTION
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

// REGISTER 
export const registerUser = async (data) => {
  const res = await axios.post(`${BASE_URL}/register`, data);
  return res.data;
};

// LOGIN 
export const loginUser = async (data) => {
  const res = await axios.post(`${BASE_URL}/login`, data);

  // TOKEN SAVE (IMPORTANT)
  localStorage.setItem("token", res.data.access_token);
  localStorage.setItem("role", res.data.role);

  return res.data;
};

export const getCountryFilters = async () => {
  const res = await axios.get(
    `${BASE_URL}/country/filters`,
    getAuthHeader()
  );
  return res.data;
};

export const getCountryArrivals = async (params) => {
  const res = await axios.get(
    `${BASE_URL}/country/search`,
    {
      params,
      ...getAuthHeader()
    }
  );
  return res.data;
};

export const getCountryCompare = async () => {
  const res = await axios.get(
    `${BASE_URL}/country/compare-years`,
    getAuthHeader()
  );
  return res.data;
};