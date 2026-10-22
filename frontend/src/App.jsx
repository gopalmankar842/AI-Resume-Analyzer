import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Analyze from "./pages/Analyze";
import ATSChecker from "./pages/ATSChecker";
import History from "./pages/History";
import Recommendations from "./pages/Recommendations";
import Interview from "./pages/Interview";
import ProtectRoute from "./ProtectRoute";
import Home from "./pages/Home";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Home/>}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/dashboard"
          element={
            <ProtectRoute>
            <Dashboard />
            </ProtectRoute>
          }
        />
        <Route
          path="/analyze"
          element={
            <ProtectRoute>
            <Analyze />
            </ProtectRoute>
          }
        />

        <Route
          path="/ats-checker"
          element={
            <ProtectRoute>
              <ATSChecker />
            </ProtectRoute>
          }
        />
        
        <Route
          path="/history"
          element={
            <ProtectRoute>
            <History />
            </ProtectRoute>
          }
        />
        
        <Route
          path="/recommendations"
          element={
            <ProtectRoute>
            <Recommendations />
            </ProtectRoute>
          }
        />
        
        <Route
          path="/interview"
          element={
            <ProtectRoute>
            <Interview />
            </ProtectRoute>
          }
        />
      
      </Routes>

    </BrowserRouter>
  );
}

export default App;