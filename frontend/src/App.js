import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";

import MainDashboard from "./pages/MainDashboard";
import Tourism from "./pages/Tourism";
import Vegetable from "./pages/Vegetable";

import AdminDashboard from "./pages/AdminDashboard";
import ViewDashboard from "./pages/ViewDashboard";

/* PRIVATE ROUTE */
function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/" />;
  }

  return children;
}

/* PUBLIC ROUTE */
function PublicRoute({ children }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) return children;

  if (role === "admin") return <Navigate to="/admin" />;
  if (role === "viewer") return <Navigate to="/viewer" />;

  return <Navigate to="/dashboard" />;
}

/*  APP */
function App() {
  const role = localStorage.getItem("role");

  return (
    <BrowserRouter>
      <Routes>

        {/* PUBLIC */}
        <Route
          path="/"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />

        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />

        {/* PROTECTED */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <MainDashboard />
            </PrivateRoute>
          }
        />

        <Route
          path="/tourism"
          element={
            <PrivateRoute>
              <Tourism />
            </PrivateRoute>
          }
        />

        <Route
          path="/vegetable"
          element={
            <PrivateRoute>
              <Vegetable />
            </PrivateRoute>
          }
        />

        {/* ROLE BASED ROUTES */}
        <Route
          path="/admin"
          element={
            role === "admin" ? (
              <PrivateRoute>
                <AdminDashboard />
              </PrivateRoute>
            ) : (
              <Navigate to="/" />
            )
          }
        />

        <Route
          path="/viewer"
          element={
            role === "viewer" ? (
              <PrivateRoute>
                <ViewDashboard />
              </PrivateRoute>
            ) : (
              <Navigate to="/" />
            )
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;