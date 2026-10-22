import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setMessage("");

      const response = await axios.post(
        "http://127.0.0.1:8000/auth/login",
        {
          email,
          password,
        }
      );

      console.log(response.data);

      const token =
        response.data.access_token ||
        response.data.token;

      if (token) {
        localStorage.setItem("token", token);

        setMessage("Login successful!");

        navigate("/dashboard");
      } else {
        setMessage("Login failed. Token not received.");
      }

    } catch (error) {
      console.error(error);

      setMessage(
        error.response?.data?.detail ||
        "Invalid email or password."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      {/* BACKGROUND EFFECTS */}

      <div className="login-glow login-glow-one"></div>

      <div className="login-glow login-glow-two"></div>


      {/* LOGIN CONTAINER */}

      <div className="login-container">


        {/* BRAND */}

        <div className="login-brand">

          <div className="login-logo">
            AI
          </div>

          <div>
            <h1>Resume Analyzer</h1>

            <p>
              AI-powered career assistant
            </p>
          </div>

        </div>


        {/* LOGIN CARD */}

        <div className="login-card">

          {/* HEADER */}

          <div className="login-header">

            <div className="login-icon">
              🔐
            </div>

            <h2>
              Welcome Back
            </h2>

            <p>
              Sign in to continue analyzing your resume.
            </p>

          </div>


          {/* FORM */}

          <form onSubmit={handleLogin}>

            {/* EMAIL */}

            <div className="form-group">

              <label htmlFor="email">
                Email Address
              </label>

              <div className="input-wrapper">

                <span className="input-icon">
                  ✉
                </span>

                <input
                  id="email"
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

            <div className="form-group">

              <label htmlFor="password">
                Password
              </label>

              <div className="input-wrapper">

                <span className="input-icon">
                  🔒
                </span>

                <input
                  id="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
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


            {/* LOGIN BUTTON */}

            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="login-spinner"></span>
                  Signing in...
                </>
              ) : (
                <>
                  Sign In →
                </>
              )}

            </button>

          </form>


          {/* MESSAGE */}

          {message && (
            <div
              className={`login-message ${
                message.includes("successful")
                  ? "success"
                  : "error"
              }`}
            >
              {message}
            </div>
          )}


          {/* REGISTER */}

          <div className="register-section">

            <span>
              Don't have an account?
            </span>

            <button
              type="button"
              onClick={() => navigate("/register")}
            >
              Create Account
            </button>

          </div>


          {/* FEATURES */}

          <div className="login-features">

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
              Interview Preparation
            </div>

          </div>

        </div>


        {/* FOOTER */}

        <p className="login-footer">
          AI Resume Analyzer • Build your career with AI
        </p>

      </div>

    </div>
  );
}

export default Login;