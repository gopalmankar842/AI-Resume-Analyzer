import { useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();

  const token = localStorage.getItem("token");

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar">

      <div
        className="navbar-logo"
        onClick={() =>
          navigate(token ? "/dashboard" : "/")
        }
      >
        AI Resume Analyzer
      </div>

      {token && (
        <div className="navbar-links">

          <button onClick={() => navigate("/dashboard")}>
            Dashboard
          </button>

          <button onClick={() => navigate("/analyze")}>
            Analyze
          </button>

          <button onClick={() => navigate("/history")}>
            History
          </button>

          <button onClick={() => navigate("/recommendations")}>
            Recommendations
          </button>

          <button onClick={() => navigate("/interview")}>
            Interview
          </button>

          <button onClick={logout}>
            Logout
          </button>

        </div>
      )}

    </nav>
  );
}

export default Navbar;