import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";
import "./Register.css";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  
  const handleRegister = async (e) => {
    e.preventDefault();

    if (loading) return;

    try {
      setLoading(true);
      setMessage("");

      const response = await API.post("/auth/register", {
        name,
        email,
        password,
      });

      console.log("Registration response:", response.data);
      setMessage("Registration successful!");

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (error) {
      console.error("Registration error:", error);

      setMessage(
        error.response?.data?.detail ||
        error.message ||
        "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="register-page">

      {/* =========================
          BACKGROUND EFFECTS
      ========================= */}

      <div className="register-glow register-glow-one"></div>

      <div className="register-glow register-glow-two"></div>


      {/* =========================
          CONTAINER
      ========================= */}

      <div className="register-container">


        {/* =========================
            BRAND
        ========================= */}

        <div className="register-brand">

          <div className="register-logo">
            AI
          </div>

          <div>
            <h1>Resume Analyzer</h1>

            <p>
              AI-powered career assistant
            </p>
          </div>

        </div>


        {/* =========================
            REGISTER CARD
        ========================= */}

        <div className="register-card">


          {/* HEADER */}

          <div className="register-header">

            <div className="register-icon">
              🚀
            </div>

            <h2>
              Create Your Account
            </h2>

            <p>
              Start improving your resume with AI.
            </p>

          </div>


          {/* =========================
              FORM
          ========================= */}

          <form onSubmit={handleRegister}>

            {/* NAME */}

            <div className="register-form-group">

              <label htmlFor="name">
                Full Name
              </label>

              <div className="register-input-wrapper">

                <span className="register-input-icon">
                  ◉
                </span>

                <input
                  id="name"
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) =>
                    setName(e.target.value)
                  }
                  required
                />

              </div>

            </div>


            {/* EMAIL */}

            <div className="register-form-group">

              <label htmlFor="register-email">
                Email Address
              </label>

              <div className="register-input-wrapper">

                <span className="register-input-icon">
                  ✉
                </span>

                <input
                  id="register-email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  required
                />

              </div>

            </div>


            {/* PASSWORD */}

            <div className="register-form-group">

              <label htmlFor="register-password">
                Password
              </label>

              <div className="register-input-wrapper">

                <span className="register-input-icon">
                  🔒
                </span>

                <input
                  id="register-password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Create a password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  required
                />

                <button
                  type="button"
                  className="register-password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? "🙈" : "👁"}
                </button>

              </div>

            </div>


            {/* REGISTER BUTTON */}

            <button
              type="submit"
              className="register-button"
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="register-spinner"></span>
                  Creating Account...
                </>
              ) : (
                <>
                  Create Account →
                </>
              )}

            </button>

          </form>


          {/* =========================
              MESSAGE
          ========================= */}

          {message && (
            <div
              className={`register-message ${
                message.includes("successful")
                  ? "success"
                  : "error"
              }`}
            >
              {message}
            </div>
          )}


          {/* =========================
              LOGIN LINK
          ========================= */}

          <div className="login-section">

            <span>
              Already have an account?
            </span>

            <button
              type="button"
              onClick={() => navigate("/login")}
            >
              Sign In
            </button>

          </div>


          {/* =========================
              FEATURES
          ========================= */}

          <div className="register-features">

            <div>
              <span>✓</span>
              AI Resume Analysis
            </div>

            <div>
              <span>✓</span>
              Job Match Scoring
            </div>

            <div>
              <span>✓</span>
              Career Recommendations
            </div>

          </div>

        </div>


        {/* =========================
            FOOTER
        ========================= */}

        <p className="register-footer">
          AI Resume Analyzer • Build your career with AI
        </p>

      </div>

    </div>
  );
}

export default Register;