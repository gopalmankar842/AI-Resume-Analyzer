import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const [sidebarOpen, setSidebarOpen] = useState(false);

  // =========================
  // NAVIGATION
  // =========================

  const goToPage = (path) => {
    navigate(path);
    setSidebarOpen(false);
  };

  // =========================
  // LOGOUT
  // =========================

  const logout = () => {
    localStorage.removeItem("token");
    setSidebarOpen(false);
    navigate("/login");
  };

  return (
    <div className="dashboard-page">

      {/* =========================
          MOBILE MENU BUTTON
      ========================= */}

      <button
        type="button"
        className="mobile-menu-button"
        onClick={() => {
          console.log("MENU CLICKED");
          setSidebarOpen((previous) => !previous);
        }}
        aria-label="Open navigation menu"
      >
        ☰
      </button>


      {/* =========================
          MOBILE OVERLAY
      ========================= */}

      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}


      {/* =========================
          SIDEBAR
      ========================= */}

      <aside
        className={`dashboard-sidebar ${
          sidebarOpen ? "sidebar-open" : ""
        }`}
      >

        {/* LOGO */}

        <div className="sidebar-logo">

          <div className="logo-icon">
            AI
          </div>

          <div>
            <h2>Resume</h2>
            <span>Analyzer</span>
          </div>

        </div>


        {/* MAIN MENU */}

        <div className="sidebar-section">

          <p className="sidebar-title">
            MAIN MENU
          </p>


          <button
            type="button"
            className="sidebar-link active"
            onClick={() => goToPage("/dashboard")}
          >
            <span>⌂</span>
            Dashboard
          </button>


          <button
            type="button"
            className="sidebar-link"
            onClick={() => goToPage("/analyze")}
          >
            <span>▣</span>
            Upload & Analyze
          </button>


          <button
            type="button"
            className="sidebar-link"
            onClick={() => goToPage("/history")}
          >
            <span>◷</span>
            Analysis History
          </button>


          <button
            type="button"
            className="sidebar-link"
            onClick={() => goToPage("/recommendations")}
          >
            <span>◎</span>
            Recommendations
          </button>


          <button
            type="button"
            className="sidebar-link"
            onClick={() => goToPage("/interview")}
          >
            <span>✦</span>
            Interview Prep
          </button>

          <button
            type="button"
            className="sidebar-link"
            onClick={() => goToPage("/ats-checker")}
          >
            <span>▣</span>
            ATS Score Checker
          </button>

        </div>

          


        {/* BOTTOM MENU */}

        <div className="sidebar-bottom">

          <button
            type="button"
            className="sidebar-link"
            onClick={() =>
              alert("Profile settings coming soon.")
            }
          >
            <span>◉</span>
            Profile
          </button>


          <button
            type="button"
            className="sidebar-link"
            onClick={() =>
              alert("Settings coming soon.")
            }
          >
            <span>⚙</span>
            Settings
          </button>


          <button
            type="button"
            className="sidebar-link logout-link"
            onClick={logout}
          >
            <span>↪</span>
            Logout
          </button>

        </div>

      </aside>


      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="dashboard-main">


        {/* =========================
            TOP BAR
        ========================= */}

        <header className="dashboard-topbar">

          <div>
            <span className="breadcrumb">
              Dashboard
            </span>
          </div>


          <div className="topbar-actions">

            <button
              type="button"
              className="icon-button"
              title="Notifications"
            >
              ♢
            </button>


            <div className="user-avatar">
              G
            </div>

          </div>

        </header>


        {/* =========================
            WELCOME BANNER
        ========================= */}

        <section className="welcome-banner">

          <div className="welcome-text">

            <span className="welcome-small">
              AI Resume Analyzer
            </span>

            <h1>
              Welcome back 👋
            </h1>

            <p>
              Ready to improve your resume and land
              your next opportunity?
            </p>

          </div>


          <button
            type="button"
            className="new-analysis-button"
            onClick={() => goToPage("/analyze")}
          >
            ✨ New Analysis
          </button>

        </section>


        {/* =========================
            STATISTICS
        ========================= */}

        <section className="stats-grid">

          <div className="stat-card">

            <div className="stat-top">

              <span>
                Total Analyses
              </span>

              <div className="stat-icon blue">
                ◫
              </div>

            </div>

            <h2>—</h2>

            <p>
              Your resume analyses
            </p>

          </div>


          <div className="stat-card">

            <div className="stat-top">

              <span>
                Average Match
              </span>

              <div className="stat-icon green">
                ◎
              </div>

            </div>

            <h2>—</h2>

            <p>
              Overall job match score
            </p>

          </div>


          <div className="stat-card">

            <div className="stat-top">

              <span>
                Resumes Analyzed
              </span>

              <div className="stat-icon purple">
                ▤
              </div>

            </div>

            <h2>—</h2>

            <p>
              Resumes uploaded
            </p>

          </div>


          <div className="stat-card">

            <div className="stat-top">

              <span>
                Skills Identified
              </span>

              <div className="stat-icon orange">
                ◈
              </div>

            </div>

            <h2>—</h2>

            <p>
              Skills from your analyses
            </p>

          </div>

        </section>


        {/* =========================
            QUICK ACTIONS
        ========================= */}

        <section className="section-heading">

          <div>

            <h2>
              What would you like to do?
            </h2>

            <p>
              Choose an option to continue.
            </p>

          </div>

        </section>


        <section className="action-grid">

          {/* ANALYSIS */}

          <div
            className="action-card analyze-card"
            onClick={() => goToPage("/analyze")}
          >

            <div className="action-icon">
              📄
            </div>

            <div className="action-content">

              <h3>
                Resume Analysis
              </h3>

              <p>
                Upload your resume and compare
                it with any job description.
              </p>

              <span className="action-link">
                Start Analysis →
              </span>

            </div>

          </div>


          {/* HISTORY */}

          <div
            className="action-card history-card"
            onClick={() => goToPage("/history")}
          >

            <div className="action-icon">
              📊
            </div>

            <div className="action-content">

              <h3>
                Analysis History
              </h3>

              <p>
                View your previous resume
                analysis results and scores.
              </p>

              <span className="action-link">
                View History →
              </span>

            </div>

          </div>


          {/* RECOMMENDATIONS */}

          <div
            className="action-card recommendation-card"
            onClick={() =>
              goToPage("/recommendations")
            }
          >

            <div className="action-icon">
              🎯
            </div>

            <div className="action-content">

              <h3>
                Career Recommendations
              </h3>

              <p>
                Discover skills you should improve
                for your target job.
              </p>

              <span className="action-link">
                Get Recommendations →
              </span>

            </div>

          </div>


          {/* INTERVIEW */}

          <div
            className="action-card interview-card"
            onClick={() => goToPage("/interview")}
          >

            <div className="action-icon">
              🎤
            </div>

            <div className="action-content">

              <h3>
                Interview Preparation
              </h3>

              <p>
                Practice with AI-generated
                interview questions.
              </p>

              <span className="action-link">
                Start Preparation →
              </span>

            </div>

          </div>

        </section>


        {/* =========================
            BOTTOM SECTION
        ========================= */}

        <section className="bottom-grid">

          <div className="info-card">

            <div className="info-card-header">

              <div>

                <h2>
                  🚀 Start Your Career Journey
                </h2>

                <p>
                  Analyze your resume against a
                  real job description to discover
                  where you stand.
                </p>

              </div>

            </div>


            <button
              type="button"
              className="primary-button"
              onClick={() => goToPage("/analyze")}
            >
              Analyze My Resume
            </button>

          </div>


          <div className="info-card improvement-card">

            <h2>
              🎯 Improve Your Match
            </h2>

            <p>
              Use your analysis results to identify
              missing skills and prepare for interviews.
            </p>


            <div className="improvement-steps">

              <span>
                01 Analyze
              </span>

              <span>
                02 Improve
              </span>

              <span>
                03 Prepare
              </span>

            </div>

          </div>

        </section>


        {/* FOOTER */}

        <footer className="dashboard-footer">
          AI Resume Analyzer • AI-powered career assistant
        </footer>

      </main>

    </div>
  );
}

export default Dashboard;