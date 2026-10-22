import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">

      <div className="home-content">

        <h1>AI Resume Analyzer</h1>

        <p>
          Analyze your resume, match it with job descriptions,
          discover missing skills, and prepare for interviews
          using AI.
        </p>

        <div className="home-buttons">

          <button onClick={() => navigate("/login")}>
            Login
          </button>

          <button onClick={() => navigate("/register")}>
            Create Account
          </button>

        </div>

      </div>

      <div className="home-features">

        <div className="home-feature">
          <h2>📄 Resume Analysis</h2>
          <p>
            Compare your resume with a target job description.
          </p>
        </div>

        <div className="home-feature">
          <h2>📊 Match Score</h2>
          <p>
            Get skill, semantic, and final match percentages.
          </p>
        </div>

        <div className="home-feature">
          <h2>🎯 Recommendations</h2>
          <p>
            Identify missing skills and career improvement areas.
          </p>
        </div>

        <div className="home-feature">
          <h2>🎤 Interview Preparation</h2>
          <p>
            Generate AI-powered interview questions.
          </p>
        </div>

      </div>

    </div>
  );
}

export default Home;