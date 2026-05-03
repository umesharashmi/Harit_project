import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";

import MainDashboard from "./pages/MainDashboard";
import Tourism from "./pages/Tourism";
import Vegetable from "./pages/Vegetable";

import AdminDashboard from "./pages/AdminDashboard";
import ViewDashboard from "./pages/ViewDashboard";

/* ✅ PRIVATE ROUTE */
function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return children;
}

/* ✅ ROLE ROUTE */
function RoleRoute({ children, role: allowedRole }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  if (role !== allowedRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

/* PUBLIC ROUTE */
function PublicRoute({ children }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) return children;

  if (role === "admin") return <Navigate to="/admin" replace />;
  if (role === "viewer") return <Navigate to="/viewer" replace />;

  return <Navigate to="/dashboard" replace />;
}

/* APP */
function App() {
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

        {/* PRIVATE ROUTES */}
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

        {/* ROLE BASED */}
        <Route
          path="/admin"
          element={
            <RoleRoute role="admin">
              <AdminDashboard />
            </RoleRoute>
          }
        />

        <Route
          path="/viewer"
          element={
            <RoleRoute role="viewer">
              <ViewDashboard />
            </RoleRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;